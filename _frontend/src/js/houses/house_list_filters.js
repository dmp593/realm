document.addEventListener('DOMContentLoaded', function () {
    const districtSelect = document.getElementById('district-select')
    const municipalitySelect = document.getElementById('municipality-select')
    const parishSelect = document.getElementById('parish-select')
    const localeSelect = document.getElementById('locale-select')

    if (! districtSelect.value) {
        municipalitySelect.setAttribute('disabled', 'disabled')
        parishSelect.setAttribute('disabled', 'disabled')
        localeSelect.setAttribute('disabled', 'disabled')
    }

    districtSelect.addEventListener('change', function () {
        const selectedDistrict = this.value
        
        Array.from(municipalitySelect.options).forEach(option => {
            option.style.display = option.getAttribute('data-district') === selectedDistrict ? 'block' : 'none'
        })

        municipalitySelect.removeAttribute('disabled')
        municipalitySelect.value = ''
    })

    municipalitySelect.addEventListener('change', function () {
        const selectedMunicipality = this.value
        
        Array.from(parishSelect.options).forEach(option => {
            option.style.display = option.getAttribute('data-municipality') === selectedMunicipality ? 'block' : 'none'
        })

        parishSelect.removeAttribute('disabled')
        parishSelect.value = ''
    })

    parishSelect.addEventListener('change', function () {
        const selectedParish = this.value
        
        Array.from(localeSelect.options).forEach(option => {
            option.style.display = option.getAttribute('data-parish') === selectedParish ? 'block' : 'none'
        })

        localeSelect.removeAttribute('disabled')
        localeSelect.value = ''
    })

    document.getElementById('reset-filters').addEventListener('click', function() {
        window.location.href = window.location.pathname
    });
})
