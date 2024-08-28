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