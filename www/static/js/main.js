 // Suche
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="q"]');
    
    if (searchInput) {
        const movieCards = document.querySelectorAll('.movie-card-container, .col[data-searchable="true"]');
        
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase().trim();
            
            movieCards.forEach(card => {
                const titleElement = card.querySelector('.card-title, .movie-title');
                if (titleElement) {
                    const title = titleElement.innerText.toLowerCase();
                    
                    if (filter === '' || title.includes(filter)) {
                        card.style.display = "";
                        card.style.opacity = "1";
                    } else {
                        card.style.display = "none";
                        card.style.opacity = "0.3";
                    }
                }
            });
        });
    }
    
    // Initialisiere alle Karten als durchsuchbar
    document.querySelectorAll('.col').forEach(col => {
        if (col.querySelector('.card-title')) {
            col.setAttribute('data-searchable', 'true');
        }
    });
});