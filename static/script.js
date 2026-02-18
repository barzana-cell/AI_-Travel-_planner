// Existing loading logic
document.getElementById('travelForm').onsubmit = function() {
    document.getElementById('submitBtn').disabled = true;
    document.getElementById('submitBtn').innerText = "Planning...";
    document.getElementById('loader').style.display = "block";
};

// New Print Logic
function printItinerary() {
    const printContent = document.getElementById("printableArea").innerHTML;
    const originalContent = document.body.innerHTML;

    // Temporarily replace body content with just the itinerary for printing
    document.body.innerHTML = `
        <div style="padding: 40px; font-family: sans-serif;">
            <h1>My Travel Plan</h1>
            <hr>
            <div style="white-space: pre-wrap;">${printContent}</div>
        </div>
    `;

    window.print();

    // Restore the original website view
    document.body.innerHTML = originalContent;
    window.location.reload(); // Reload to re-attach button events
}