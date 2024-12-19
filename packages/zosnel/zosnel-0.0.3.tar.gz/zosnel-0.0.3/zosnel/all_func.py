'''
from main import zosnel

zosnel = zosnel()
zosnel.set_title("My Website")
zosnel.heading("Welcome!")
zosnel.para("This is a test paragraph")
zosnel.add_css("body { background-color: #f0f0f0; font-family: sans-serif;}")
zosnel.serve()
'''

from main import zosnel  # Import the ZOSNEL class

# Create an instance of the ZOSNEL class
zosnel = zosnel(port=8000)

# Set the page title
zosnel.set_title("Testing ZOSNEL Framework")

# Add HTML content
zosnel.heading("Welcome to ZOSNEL!", level=1)
zosnel.para("This paragraph is added using the 'para' method.")
zosnel.url("Click here to visit GitHub", "https://github.com")
zosnel.img("https://via.placeholder.com/150", alt="Sample Image")
zosnel.sep()
zosnel.breakline()

# Add CSS
zosnel.add_css("""
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    text-align: center;
    background-color: #f0f8ff;
}

h1 {
    color: #4CAF50;
}

button {
    padding: 10px 20px;
    margin-top: 20px;
    background-color: #007BFF;
    color: white;
    border: none;
    cursor: pointer;
}

button:hover {
    background-color: #0056b3;
}
""")

# Add JavaScript
zosnel.javascript("""
document.addEventListener("DOMContentLoaded", function() {
    alert("Hello from ZOSNEL's JavaScript!");
    console.log("JavaScript is working!");
});

function onButtonClick() {
    alert("Button clicked!");
}
""")

# Add custom HTML with inline JavaScript
zosnel.custom('<button onclick="onButtonClick()">Click Me</button>')

# Serve the site
zosnel.serve()
