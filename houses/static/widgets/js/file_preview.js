document.addEventListener('DOMContentLoaded', function() {
    const CHUNK_UPLOAD_SIZE = 4_194_304; // 4 MB chunk size (4 * 1024 * 1024)
    const CSRF_TOKEN = django.jQuery('input[name="csrfmiddlewaretoken"]').val();

    // Create a single reusable modal element
    const $modal = django.jQuery('<div class="modal"><span class="close">&times;</span><div class="modal-content"></div></div>');
    django.jQuery('body').append($modal);
    const $modalContent = $modal.find('.modal-content');
    const $closeModalButton = $modal.find('.close');

    function openModal($content) {
        if (!['IMG', 'VIDEO', 'IFRAME'].includes($content.prop('tagName'))) {
            return;
        }
        const $clone = $content.clone().css({
            width: '100%',
            height: '90vh',
            objectFit: 'contain'
        });
        $modalContent.empty().append($clone);
        $modal.show();
    }

    function closeModal() {
        $modal.hide();
        $modalContent.empty();
    }

    $closeModalButton.on('click', closeModal);
    django.jQuery(window).on('click', function(event) {
        if (django.jQuery(event.target).is($modal)) {
            closeModal();
        }
    });

    async function uploadFileInChunks($fileInput, url, method) {
        const file = $fileInput[0].files[0];
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

        console.log('Upload complete');
        const tmpFileInputName = $fileInput.attr('name').replace(/file$/, 'tmp_file');
        let $tmpFileInput = django.jQuery(`input[name="${tmpFileInputName}"]`);

        if (!$tmpFileInput.length) {
            $tmpFileInput = django.jQuery('<input>', {
                type: 'hidden',
                name: tmpFileInputName
            });
            $fileInput.closest('.file-preview-container .clearable-file-input').append($tmpFileInput);
        }

        $tmpFileInput.val(file_url);
        $fileInput.val(null);
    }

    function initializeOnChangeShowFilePreview($fileInput) {
        $fileInput.on('change', async function(event) {
            const dataTransfer = new DataTransfer();
            for (let index = 1; index < event.target.files.length; ++index) {
                dataTransfer.items.add(event.target.files[index]);
            }

            const file = event.target.files[0];
            const $container = $fileInput.closest('.file-preview-container');
            const $filePreview = $container.find('.file-preview');
            let $preview = $filePreview.children().first();

            if ($preview.length) {
                $filePreview.empty();
            }

            if (file.type.startsWith('image/')) {
                $preview = django.jQuery('<img>', { loading: 'lazy' });
            } else if (file.type.startsWith('video/')) {
                $preview = django.jQuery('<video>', { controls: true });
            } else if (file.type === 'application/pdf') {
                $preview = django.jQuery('<iframe>');
            } else {
                $preview = django.jQuery('<p>').text(file.name);
            }

            $preview.addClass('file-preview-element').css({
                width: '250px',
                height: '150px',
                objectFit: 'cover',
                borderRadius: '5px',
                transition: 'transform 0.3s ease',
                cursor: 'pointer'
            });

            $filePreview.append($preview);

            if (file.type === 'application/pdf') {
                $filePreview.css('position', 'relative');
                const $clickLayer = django.jQuery('<div>', { class: 'file-preview-click-layer' });
                $container.find('.file-preview').append($clickLayer);
                $clickLayer.on('click', function() { openModal($preview); });
            } else {
                $preview.on('click', function() { openModal($preview); });
            }

            $preview.attr('src', URL.createObjectURL(file)).show();

            const uploadUrl = $fileInput.data('chunked-upload-url');
            const uploadMethod = $fileInput.data('chunked-upload-method') || 'POST';
            await uploadFileInChunks($fileInput, uploadUrl, uploadMethod);

            if ($fileInput.prop('multiple') && dataTransfer.items.length > 0) {
                let availableContainers = django.jQuery(".inline-related:not(.empty-form):not(:has('.file-preview-element'))");
                const containersToAdd = dataTransfer.items.length - availableContainers.length;

                if (containersToAdd > 0) {
                    const $addRow = django.jQuery('.add-row a');
                    $addRow.trigger('click');
                    availableContainers = django.jQuery(".inline-related:not(.empty-form):not(:has('.file-preview-element'))");
                }

                const $newFileInput = availableContainers.first().find('.file-preview-container input[type="file"]');
                $newFileInput[0].files = dataTransfer.files;
                $newFileInput.trigger('change');
            }
        });
    }

    function initializeOnClickOpenModal($fileInput) {
        const $container = $fileInput.closest('.file-preview-container');
        const $filePreviewClickLayer = $container.find('.file-preview-click-layer');
        const $filePreview = $container.find('.file-preview-element');

        if ($filePreview.length) {
            ($filePreviewClickLayer.length ? $filePreviewClickLayer : $filePreview).on('click', function() {
                openModal($filePreview);
            });
        }
    }

    function initializeFileInput($fileInput) {
        initializeOnChangeShowFilePreview($fileInput);
        initializeOnClickOpenModal($fileInput);
    }

    django.jQuery('.file-preview-container input[type="file"]').each(function() {
        initializeFileInput(django.jQuery(this));
    });

    setTimeout(() => {
        const $addRow = django.jQuery('.add-row a');
        if ($addRow.length) {
            $addRow.on('click', function() {
                const $containers = django.jQuery(".inline-related:not(.empty-form):not(:has('.file-preview-element'))");
                const $lastContainer = $containers.last();
                initializeFileInput($lastContainer.find('.file-preview-container input[type="file"]'));
            });
        }
    }, 1);
});
