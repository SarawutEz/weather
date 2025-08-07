document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('city-input');
    const suggestions = document.getElementById('suggestions');

    input.addEventListener('input', async function() {
        const query = input.value.trim();
        if (query.length < 2) {
            suggestions.innerHTML = '';
            suggestions.classList.add('hidden');
            return;
        }
        // ใช้ weatherapi.com สำหรับค้นหาเมือง
        try {
            const res = await fetch(`https://api.weatherapi.com/v1/search.json?key=24b2faf291d14dc3a3a33107252907&q=${encodeURIComponent(query)}`);
            const data = await res.json();
            if (data.length > 0) {
                suggestions.innerHTML = data.map(city =>
                    `<li class="px-4 py-2 cursor-pointer hover:bg-blue-800 text-blue-200" data-city="${city.name}">${city.name}, ${city.country}</li>`
                ).join('');
                suggestions.classList.remove('hidden');
            } else {
                suggestions.innerHTML = '';
                suggestions.classList.add('hidden');
            }
        } catch (error) {
            suggestions.innerHTML = '';
            suggestions.classList.add('hidden');
            console.error('Error fetching city suggestions:', error);
        }
    });

    suggestions.addEventListener('click', function(e) {
        if (e.target && e.target.dataset.city) {
            input.value = e.target.dataset.city;
            suggestions.innerHTML = '';
            suggestions.classList.add('hidden');
        }
    });

    document.addEventListener('click', function(e) {
        if (!input.contains(e.target) && !suggestions.contains(e.target)) {
            suggestions.innerHTML = '';
            suggestions.classList.add('hidden');
        }
    });
});
