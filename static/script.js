// Global variable to store current password
let currentPassword = '';

// Update length display
function updateLength(value) {
    document.getElementById('lengthValue').textContent = value;
}

// Generate password function
function generatePassword() {
    const passwordDisplay = document.getElementById('passwordDisplay');
    const copyBtn = document.getElementById('copyBtn');
    
    // Show loading
    passwordDisplay.textContent = 'Generating...';
    passwordDisplay.classList.remove('active');
    
    // Get options from UI
    const length = parseInt(document.getElementById('lengthSlider').value);
    const uppercase = document.getElementById('uppercaseCheck').checked;
    const lowercase = document.getElementById('lowercaseCheck').checked;
    const digits = document.getElementById('digitsCheck').checked;
    const symbols = document.getElementById('symbolsCheck').checked;
    
    // Call API
    fetch('/api/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            length: length,
            uppercase: uppercase,
            lowercase: lowercase,
            digits: digits,
            symbols: symbols
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            // Store and display password
            currentPassword = result.password;
            passwordDisplay.textContent = currentPassword;
            passwordDisplay.classList.add('active');
            copyBtn.disabled = false;
            copyBtn.textContent = '📋 Copy';
            copyBtn.classList.remove('copied');
        } else {
            passwordDisplay.textContent = '❌ Error';
            copyBtn.disabled = true;
            currentPassword = '';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        passwordDisplay.textContent = '❌ Error: ' + error.message;
        copyBtn.disabled = true;
        currentPassword = '';
    });
}

// Copy to clipboard function with fallback
function copyPassword() {
    const copyBtn = document.getElementById('copyBtn');
    
    if (!currentPassword) {
        alert('No password to copy!');
        return;
    }
    
    // Modern way - Clipboard API
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(currentPassword).then(() => {
            showCopySuccess();
        }).catch(err => {
            console.error('Clipboard API failed:', err);
            fallbackCopy();
        });
    } else {
        // Fallback for older browsers or HTTP
        fallbackCopy();
    }
}

// Fallback copy method
function fallbackCopy() {
    const passwordDisplay = document.getElementById('passwordDisplay');
    const textArea = document.createElement('textarea');
    textArea.value = currentPassword;
    textArea.style.position = 'fixed';
    textArea.style.left = '-9999px';
    document.body.appendChild(textArea);
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess();
        } else {
            alert('Failed to copy password. Please copy manually.');
        }
    } catch (err) {
        console.error('Fallback copy failed:', err);
        alert('Failed to copy password. Please copy manually.');
    }
    
    document.body.removeChild(textArea);
}

// Show copy success feedback
function showCopySuccess() {
    const copyBtn = document.getElementById('copyBtn');
    copyBtn.textContent = '✅ Copied!';
    copyBtn.classList.add('copied');
    
    setTimeout(() => {
        copyBtn.textContent = '📋 Copy';
        copyBtn.classList.remove('copied');
    }, 2000);
}

