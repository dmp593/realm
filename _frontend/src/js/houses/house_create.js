document.addEventListener('DOMContentLoaded', () => {
    const dataTransfer = new DataTransfer();
    const progressBar = document.getElementById('progress-bar');
    const submitButton = document.querySelector('button[type="submit"]');

    const maxVideoPreviewFileSize = 250 * 1024 * 1024; // 250MB

    document.getElementById('files').addEventListener('change', function(event) {
        const previewContainer = document.getElementById('preview-container');
        Array.from(event.target.files).forEach((file, index) => {
            dataTransfer.items.add(file);
            const previewElement = document.createElement('div');
            previewElement.classList.add('relative', 'w-full', 'h-32', 'rounded-lg', 'shadow-md', 'overflow-hidden');
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.classList.add('w-full', 'h-full', 'object-cover');
                    previewElement.appendChild(img);
                };
                reader.readAsDataURL(file);
            } else if (file.type.startsWith('video/')) {
                if (file.size < maxVideoPreviewFileSize) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const video = document.createElement('video');
                        video.src = e.target.result;
                        video.classList.add('w-full', 'h-full', 'object-cover');
                        video.controls = true; // Add controls to the video
                        previewElement.appendChild(video);
                    };
                    reader.readAsDataURL(file);
                } else {
                    const icon = document.createElement('i');
                    icon.classList.add('ph-bold', 'ph-video', 'text-4xl', 'text-gray-500', 'flex', 'items-center', 'justify-center', 'w-full', 'h-full');
                    previewElement.appendChild(icon);
                }
            } else {
                const icon = document.createElement('i');
                icon.classList.add('ph-bold', 'ph-file', 'text-4xl', 'text-gray-500', 'flex', 'items-center', 'justify-center', 'w-full', 'h-full');
                previewElement.appendChild(icon);
            }
            const removeButton = document.createElement('span');
            removeButton.innerHTML = '<i class="ph-bold ph-x"></i>';
            removeButton.classList.add('absolute', 'top-1', 'right-1', 'bg-red-500', 'text-white', 'rounded-full', 'w-6', 'h-6', 'flex', 'items-center', 'justify-center', 'cursor-pointer', 'z-50');
            removeButton.addEventListener('click', function() {
                previewElement.remove();
                dataTransfer.items.remove(index);
                event.target.files = dataTransfer.files;
            });
            previewElement.appendChild(removeButton);
            previewContainer.appendChild(previewElement);
        });
        event.target.files = dataTransfer.files;
    });

    function uploadFiles(houseId) {
        return new Promise((resolve, reject) => {
            const files = dataTransfer.files;
            const chunkSize = 1024 * 1024; // 1MB
            const maxConcurrentUploads = 3; // Limit the number of concurrent uploads
            let activeUploads = 0;
            const queue = [];
            let totalUploaded = 0;
            const totalSize = Array.from(files).reduce((acc, file) => acc + file.size, 0);

            function uploadChunk(file, chunkIndex, totalChunks, fileId, houseId, filename, order) {
                const chunk = file.slice(chunkIndex * chunkSize, (chunkIndex + 1) * chunkSize);
                const formData = new FormData();
                formData.append('file', chunk);
                formData.append('chunkIndex', chunkIndex);
                formData.append('totalChunks', totalChunks);
                formData.append('fileId', fileId);
                formData.append('houseId', houseId);
                formData.append('filename', filename);
                formData.append('order', order);

                fetch("{% url 'upload_chunk' %}", {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': '{{ csrf_token }}'
                    }
                }).then(response => response.json()).then(data => {
                    if (data.status === 'ok') {
                        totalUploaded += chunk.size;
                        progressBar.style.width = `${(totalUploaded / totalSize) * 100}%`;
                        if (chunkIndex === totalChunks - 1) {
                            console.log(`File ${filename} uploaded successfully.`);
                        }
                    }
                    activeUploads--;
                    processQueue();
                }).catch(error => {
                    console.error('Error uploading chunk:', error);
                    activeUploads--;
                    processQueue();
                });
            }

            function processQueue() {
                while (activeUploads < maxConcurrentUploads && queue.length > 0) {
                    const { file, chunkIndex, totalChunks, fileId, houseId, filename, order } = queue.shift();
                    activeUploads++;
                    uploadChunk(file, chunkIndex, totalChunks, fileId, houseId, filename, order);
                }
                if (queue.length === 0 && activeUploads === 0) {
                    resolve();
                }
            }

            Array.from(files).forEach((file, index) => {
                const totalChunks = Math.ceil(file.size / chunkSize);
                const fileId = `house_${index}`;
                for (let i = 0; i < totalChunks; i++) {
                    queue.push({
                        file,
                        chunkIndex: i,
                        totalChunks,
                        fileId,
                        houseId,
                        filename: file.name,
                        order: index + 1
                    });
                }
            });

            processQueue();
        });
    }

    document.getElementById('house-form').addEventListener('submit', function(event) {
        event.preventDefault();

        submitButton.classList.add('disabled');
        submitButton.disabled = true;
        submitButton.innerHTML = 'A processar...';

        const formData = new FormData(this);
        fetch("{% url 'house_create' %}", {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'
            }
        }).then(response => response.json()).then(data => {
            if (data.house_id) {
                const houseId = data.house_id;
                uploadFiles(houseId).then(() => {
                    window.location.href = data.success_url;
                });
            } else if (data.errors) {
                // Handle form errors
                const errorFields = Object.keys(data.errors);
                errorFields.forEach(field => {
                    const errorContainer = document.getElementById(`error_${field}`);
                    errorContainer.innerHTML = data.errors[field].join('<br>');
                });
            }
        }).catch(error => {
            console.error('Error creating house:', error);
        }).finally(() => {
            submitButton.classList.remove('disabled');
            submitButton.disabled = false;
            submitButton.innerHTML = 'Criar Casa';
        });
    });
});