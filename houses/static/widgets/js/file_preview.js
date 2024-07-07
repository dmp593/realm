document.addEventListener("DOMContentLoaded", function() {
    const CHUNK_UPLOAD_SIZE = 4_194_304; // 4 MB chunk size (4 * 1024 * 1024)
    const CSRF_TOKEN = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // Create a single reusable modal element
    const modal = document.createElement('div');
    modal.classList.add('modal');

    modal.innerHTML = `
        <span class="close">&times;</span>
        <div class="modal-content"></div>
    `;

    document.body.appendChild(modal);

    const modalContent = modal.querySelector('.modal-content');
    const closeModalButton = modal.querySelector('.close');

    function openModal(content) {
        if (!['IMG', 'VIDEO', 'IFRAME'].includes(content.tagName)) {
            return;
        }

        const clone = content.cloneNode(true);
        clone.style.width = '100%';
        clone.style.height = '90vh';
        clone.style.objectFit = 'contain';

        modalContent.innerHTML = '';
        modalContent.appendChild(clone);
        modal.style.display = 'block';
    }

    function closeModal() {
        modal.style.display = 'none';
        modal.querySelector('.modal-content').innerHTML = '';
    }

    closeModalButton.addEventListener('click', closeModal);
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    async function uploadFileInChunks(fileInput, url, method) {
        const file = fileInput.files[0];
        const totalChunks = Math.ceil(file.size / CHUNK_UPLOAD_SIZE);
        const fileId = crypto.randomUUID();

        let file_url = null;

        for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
            const start = chunkIndex * CHUNK_UPLOAD_SIZE;
            const end = Math.min(start + CHUNK_UPLOAD_SIZE, file.size);
            const chunk = file.slice(start, end);

            const formData = new FormData();
            formData.append('file', chunk);
            formData.append('fileId', fileId);
            formData.append('fileName', file.name);
            formData.append('chunkIndex', chunkIndex);
            formData.append('totalChunks', totalChunks);
            formData.append('csrfmiddlewaretoken', CSRF_TOKEN);

            const response = await fetch(url, {
                method: method,
                body: formData,
                headers: { 'X-CSRFToken': CSRF_TOKEN }
            });

            if (!response.ok) {
                console.error('Upload failed', await response.json());
                return;
            }

            if (chunkIndex + 1 === totalChunks) {
                const json = await response.json();
                file_url = json.url;
            }
        }

        // All chunks uploaded
        console.log('Upload complete');

        // Update the tmp_file input
        const tmpFileInputName = fileInput.getAttribute('name').replace(/file$/, 'tmp_file');
        let tmpFileInput = document.querySelector(`input[name="${tmpFileInputName}"]`);

        if (!tmpFileInput) {
            tmpFileInput = document.createElement('input');
            tmpFileInput.setAttribute('type', 'hidden');
            tmpFileInput.setAttribute('name', tmpFileInputName);

            fileInput.closest('.file-preview-container .clearable-file-input').appendChild(tmpFileInput);
        }

        tmpFileInput.value = file_url;
        fileInput.value = null;
    }

    function initializeFilePreview(fileInput) {
        fileInput.addEventListener("change", async function(event) {
            const dataTransfer = new DataTransfer();

            for (let index = 1; index < event.target.files.length; ++index) {
                dataTransfer.items.add(event.target.files[index])
            }

            const file = event.target.files[0];
            const container = event.target.closest('.file-preview-container');

            const filePreview = container.querySelector('.file-preview');

            let preview = filePreview.firstChild;

            if (!!preview) {
                filePreview.innerHTML = '';
            }

            if (file.type.startsWith('image/')) {
                preview = document.createElement('img');
                preview.loading = 'lazy';
            } else if (file.type.startsWith('video/')) {
                preview = document.createElement('video');
                preview.controls = true;
            } else if (file.type === 'application/pdf') {
                preview = document.createElement('iframe');
            } else {
                preview = document.createElement('p');
                preview.textContent = file.name;
            }

            preview.className = 'file-preview-element';
            preview.style.width = '250px';
            preview.style.height = '150px';
            preview.style.objectFit = 'cover';
            preview.style.borderRadius = '5px';
            preview.style.transition = 'transform 0.3s ease';
            preview.style.cursor = 'pointer';

            filePreview.appendChild(preview);

            if (file.type === 'application/pdf') {
                filePreview.style.position = 'relative';

                const wrapper = document.createElement('div');
                wrapper.className = 'file-preview-element-wrapper';

                container.querySelector('.file-preview').appendChild(wrapper)

                wrapper.addEventListener('click', function(e) {
                    openModal(preview);
                });

            } else {
                preview.addEventListener('click', function(e) {
                    openModal(preview);
                });
            }

            preview.src = URL.createObjectURL(file);
            preview.style.display = 'block';

            // Start chunked upload
            const uploadUrl = fileInput.getAttribute('data-chunked-upload-url');
            const uploadMethod = fileInput.getAttribute('data-chunked-upload-method') || 'POST';

            await uploadFileInChunks(fileInput, uploadUrl, uploadMethod);

            // Handle multiple file uploads
            if (fileInput.multiple && dataTransfer.items.length > 0) {
                let availableContainers = django.jQuery(".inline-related:not(.empty-form):not(:has('.file-preview-element'))")

                const containersToAdd = dataTransfer.items.length - availableContainers.length
                if (containersToAdd > 0) {
                    const addRow = document.querySelector('.add-row a')
                    addRow.dispatchEvent(new Event('click'))

                    availableContainers = django.jQuery(".inline-related:not(.empty-form):not(:has('.file-preview-element'))")
                }

                const fileInput = availableContainers.get(0).querySelector('.file-preview-container input[type="file"]')
                fileInput.files = dataTransfer.files
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    }

    function init(fileInput) {
        initializeFilePreview(fileInput);

        // Handle existing previews
        const container = fileInput.closest('.file-preview-container');

        let filePreviewWrapper = container.querySelector('.file-preview-element-wrapper');
        let filePreview = container.querySelector('.file-preview-element');

        if (filePreview) {
            (filePreviewWrapper || filePreview).addEventListener('click', function(e) {
                openModal(filePreview);
            });
        }
    }

    document.querySelectorAll('.file-preview-container input[type="file"]').forEach(init);

    setTimeout(() => {
        const addRow = document.querySelector('.add-row a')

        addRow.addEventListener('click', function () {
            const containers = django.jQuery(".inline-related:not(.empty-form):not(:has('.file-preview-element'))");
            const lastContainer = containers[containers.length - 1];

            init(
                lastContainer.querySelector('.file-preview-container input[type="file"]')
            )
        })
    }, 1)
});
