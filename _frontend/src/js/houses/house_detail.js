import('../../css/house_detail.css')


function setMapCoords(lat, lon, layer) {
    const container = document.getElementById('map-container')
    const iframe = document.getElementById('openstreetmap')
    const bbox = `${lon - 0.01},${lat - 0.01},${lon + 0.01},${lat + 0.01}`

    iframe.src = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=${layer}&marker=${lat},${lon}`
    container.classList.remove('hidden')
}

async function geocodeAddress(address) {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
        .then(response => response.json())
        .then(data => {
            if (data.length <= 0) {
                console.log(`Address '${address}' not found.`)
                return
            }

            const lat = parseFloat(data[0].lat)
            const lon = parseFloat(data[0].lon)
            
            return {lat, lon}
        })
        .catch(error => {
            console.error('Error:', error)
            
            return { lat: null, lon: null }
        })

    return response
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Link copiado!');
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

function showToast(message) {
    const toast = document.getElementById('toast-link-shared');
    toast.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => { toast.classList.add('hidden') }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById("share-house").addEventListener("click", async () => {
        if (navigator.share) {
            try {
                await navigator.share({ title: document.title, url: window.location.href });
                console.log('Page shared successfully');
            } catch (error) {
                console.error('Error sharing the page:', error);
            }
        } else {
            console.log('Share not supported on this browser, copying URL instead');
            copyToClipboard(window.location.href);
        }
    });
})


window.setupMapAddress = async function (address) {
    const { lat, lon } = await geocodeAddress(address)
    
    if (lat && lon) {
        setMapCoords(lat, lon, 'mapnik')
    }
}
