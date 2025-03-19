document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('story-form');
    const storyContainer = document.getElementById('story-container');
    const loadingDiv = document.getElementById('loading');
    const titleElement = document.getElementById('title');
    const storyElement = document.getElementById('story');
    const scenesElement = document.getElementById('scenes');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        storyContainer.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        titleElement.textContent = '';
        storyElement.textContent = '';
        scenesElement.innerHTML = '';

        const formData = new FormData(form);

        fetch('/generate', {
            method: 'POST',
            body: formData
        }).then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            function readStream() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        console.log('Stream complete');
                        return;
                    }

                    const chunk = decoder.decode(value);
                    const events = chunk.split('\n\n');

                    events.forEach(event => {
                        if (event.trim() !== '') {
                            const [eventType, data] = event.split('\n');
                            const eventName = eventType.replace('event: ', '');
                            const eventData = data.replace('data: ', '');

                            handleEvent(eventName, eventData);
                        }
                    });

                    readStream();
                });
            }

            readStream();
        }).catch(error => {
            console.error('Error:', error);
            loadingDiv.classList.add('hidden');
            storyContainer.classList.remove('hidden');
            storyElement.innerHTML += `<p class="error">Error: ${error.message}</p>`;
        });
    });

    function handleEvent(eventName, eventData) {
        switch(eventName) {
            case 'story_start':
                console.log('Story generation started');
                break;
            case 'story':
                loadingDiv.classList.add('hidden');
                storyContainer.classList.remove('hidden');
                storyElement.textContent = eventData;
                break;
            case 'title_start':
                console.log('Title generation started');
                break;
            case 'title':
                titleElement.textContent = eventData;
                break;
            case 'scenes_start':
                console.log('Scene breakdown started');
                break;
            case 'scenes':
                scenesElement.innerHTML = '';
                eventData.split('\n').forEach((scene, index) => {
                    if (scene.trim()) {
                        const sceneDiv = document.createElement('div');
                        sceneDiv.className = 'scene';
                        sceneDiv.innerHTML = `
                            <p>${scene}</p>
                            <div id="image-${index}" class="image-placeholder">Generating image...</div>
                        `;
                        scenesElement.appendChild(sceneDiv);
                    }
                });
                break;
            case 'image':
                const imageData = JSON.parse(eventData);
                const imageContainer = document.getElementById(`image-${imageData.scene}`);
                imageContainer.innerHTML = `<img src="${imageData.url}" alt="Scene illustration">`;
                break;
            case 'image_error':
                const errorData = JSON.parse(eventData);
                const errorContainer = document.getElementById(`image-${errorData.scene}`);
                errorContainer.textContent = 'Failed to generate image';
                break;
            case 'error':
                console.error('Error:', eventData);
                loadingDiv.classList.add('hidden');
                storyContainer.classList.remove('hidden');
                storyElement.innerHTML += `<p class="error">Error: ${eventData}</p>`;
                break;
            case 'complete':
                console.log('Generation complete');
                break;
        }
    }

    document.getElementById('narration').addEventListener('change', function() {
        const promptContainer = document.getElementById('prompt-container');
        promptContainer.style.display = this.value === 'grandma' ? 'none' : 'block';
    });
});