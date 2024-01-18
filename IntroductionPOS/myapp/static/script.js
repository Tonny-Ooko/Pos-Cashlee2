
        document.addEventListener('DOMContentLoaded', function () {
            const image = document.getElementById('image');

            // Simulate a loading process (replace this with your real loading process)
            setTimeout(function () {
                image.style.display = 'block'; // Show the image
                document.querySelector('.loading-screen').style.display = 'none'; // Hide the loading screen
            }, 10000); // Simulate a 3-second loading time
        });