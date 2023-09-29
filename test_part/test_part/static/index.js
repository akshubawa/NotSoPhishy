// const hoverLink = document.querySelector('.hover-link');
// const popup = document.querySelector('.popup');

// hoverLink.addEventListener('mouseenter', () => {
//     // Extract the text from the link
//     const extractedText = hoverLink.textContent;

//     // Send the text to the backend for processing
//     fetch('http://127.0.0.1:5000/process-text', {
//         method: 'POST',
//         body: JSON.stringify({ text: extractedText }),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Display the processed data in the popup
//         document.getElementById('extracted-text').textContent = data.processedText;
//         popup.style.display = 'block';
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });

// hoverLink.addEventListener('mouseleave', () => {
//     // Hide the popup on mouse leave
//     popup.style.display = 'none';
// });

// const hoverLink = document.querySelectorAll('.hover-link');
// const popup = document.querySelector('.popup');

// const extractedText = hoverLink.textContent;

// hoverLink.addEventListener('mouseenter', () => {
//     // Display the loading message
//     document.getElementById('extracted-text').textContent = 'Loading...';

//     // Extract the text from the link
//     const extractedText = hoverLink.textContent;

//     // Send the text to the backend for processing
//     fetch('http://127.0.0.1:5000/process-text', {
//         method: 'POST',
//         body: JSON.stringify({ text: extractedText }),
//         headers: {
//             'Content-Type': 'application/json'
//         }
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Display the processed data in the popup
//         document.getElementById('extracted-text').textContent = data.processedText;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });

//     // Show the popup
//     popup.style.display = 'block';
// });

// hoverLink.addEventListener('mouseleave', () => {
//     // Hide the popup on mouse leave
//     popup.style.display = 'none';
// });

const hoverLinks = document.querySelectorAll('.hover-link');
const popup = document.querySelector('.popup');

hoverLinks.forEach((hoverLink) => {
    hoverLink.addEventListener('mouseenter', () => {
        // Display the loading message
        document.getElementById('extracted-text').textContent = 'Loading...';

        // Extract the text from the link
        const extractedText = hoverLink.textContent;

        // Send the text to the backend for processing
        fetch('http://127.0.0.1:5000/process-text', {
            method: 'POST',
            body: JSON.stringify({ text: extractedText }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Display the processed data in the popup
            document.getElementById('extracted-text').textContent = data.processedText;
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Show the popup
        popup.style.display = 'block';
    });

    hoverLink.addEventListener('mouseleave', () => {
        // Hide the popup on mouse leave
        popup.style.display = 'none';
    });
});
