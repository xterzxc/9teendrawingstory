const quotes = [
    "The buffalo inside me awakens when the poop doesn't flush the first time.",
    "I'll tell you two phrases that will open all doors for you. Off yourself and onto yourself.",
    "You don't need to change yourself for someone else, you need to change your socks.",
    "First a hook, then a deep throat.",
    "I go to the doctor and ask him how he is feeling.",
    "I was attacked by five guys. I was in the hospital on the first, second, third, fourth, and fifth.",
    "If you put butter under the sun, it becomes sunflower butter. ",
    "When I approach a queue, I never ask who’s last, because the first is always after me.",
    "I'm in glasses, and you're in the toilet.",
    "Today, big things were waiting for me, but they never happened.",
];

function displayRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const quoteElement = document.getElementById('quote');
    quoteElement.textContent = quotes[randomIndex];
}

window.onload = displayRandomQuote;

let currentPage = 1;
let hasNextPage = true;
let isThrottling = false;

window.onscroll = function() {
    if (isThrottling) return;

    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
        isThrottling = true;
        setTimeout(function() {
            loadMoreImages();
            isThrottling = false;
        }, 300);
    }
};
function loadMoreImages() {
    if (!hasNextPage) return;

    currentPage++;

    fetch(`/load-drawings/?page=${currentPage}`)
        .then(response => response.json())
        .then(data => {
            const grid = document.getElementById('grid');
            data.data.forEach(image => {
                const gridItem = document.createElement('div');
                gridItem.classList.add('grid-item');

                gridItem.innerHTML = `
                    <div class="drawing-container">
                        <img src="${image.imglink}" alt="${image.title}">
                        <div class="avatar-overlay">
                            <img class="avatar-img" src="${image.avatarlink}" alt="User Avatar">
                        </div>
                    </div>
                    <h3>${image.title}</h3>
                `;
                grid.appendChild(gridItem);
            });

            hasNextPage = data.has_next;
        })
        .catch(error => {
            console.error('Error loading more images:', error);
        });
}