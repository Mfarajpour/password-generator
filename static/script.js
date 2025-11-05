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
    const strengthSection = document.getElementById('strengthSection');
    
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
            
            // Show and update strength indicator
            strengthSection.style.display = 'block';
            updatePasswordStrength(currentPassword, result.options);
        } else {
            passwordDisplay.textContent = '❌ Error';
            copyBtn.disabled = true;
            currentPassword = '';
            strengthSection.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        passwordDisplay.textContent = '❌ Error: ' + error.message;
        copyBtn.disabled = true;
        currentPassword = '';
        strengthSection.style.display = 'none';
    });
}

// 🆕 Calculate password strength (Strict Algorithm)
function calculatePasswordStrength(password, options) {
    const length = password.length;
    let score = 0;
    
    // Count active character types
    const charTypes = [
        options.uppercase && /[A-Z]/.test(password),
        options.lowercase && /[a-z]/.test(password),
        options.digits && /[0-9]/.test(password),
        options.symbols && /[^A-Za-z0-9]/.test(password)
    ].filter(Boolean).length;
    
    // Calculate character pool size
    let poolSize = 0;
    if (options.lowercase || /[a-z]/.test(password)) poolSize += 26;
    if (options.uppercase || /[A-Z]/.test(password)) poolSize += 26;
    if (options.digits || /[0-9]/.test(password)) poolSize += 10;
    if (options.symbols || /[^A-Za-z0-9]/.test(password)) poolSize += 33;
    
    // Calculate entropy (bits)
    const entropy = length * Math.log2(poolSize || 1);
    
    // Scoring system (0-100)
    
    // 1. Length score (0-35 points) - Most important!
    if (length >= 20) score += 35;
    else if (length >= 16) score += 30;
    else if (length >= 12) score += 22;
    else if (length >= 8) score += 12;
    else if (length >= 6) score += 5;
    else score += 0; // Very dangerous!
    
    // 2. Character variety (0-30 points)
    score += charTypes * 7.5;
    
    // 3. Entropy bonus (0-25 points)
    if (entropy >= 80) score += 25;
    else if (entropy >= 60) score += 20;
    else if (entropy >= 40) score += 12;
    else if (entropy >= 28) score += 5;
    
    // 4. Uniqueness (0-10 points)
    const uniqueChars = new Set(password).size;
    const uniqueRatio = uniqueChars / length;
    if (uniqueRatio >= 0.9) score += 10;
    else if (uniqueRatio >= 0.7) score += 7;
    else if (uniqueRatio >= 0.5) score += 4;
    
    // ⚠️ Penalties for dangerous patterns
    
    // Too short with low variety
    if (length < 8 && charTypes <= 2) score = Math.min(score, 20);
    
    // Very short passwords are always very weak
    if (length < 6) score = Math.min(score, 15);
    
    // Single character type = max medium
    if (charTypes === 1) score = Math.min(score, 45);
    
    // Determine strength level (5 levels)
    let strength, strengthText, warningMessage;
    
    if (score < 25) {
        strength = 'very-weak';
        strengthText = 'Very Weak';
        warningMessage = '⚠️ Extremely unsafe! Can be cracked in seconds!';
    } else if (score < 45) {
        strength = 'weak';
        strengthText = 'Weak';
        warningMessage = '⚠️ Unsafe! Vulnerable to attacks.';
    } else if (score < 65) {
        strength = 'medium';
        strengthText = 'Medium';
        warningMessage = '⚡ Acceptable, but could be stronger.';
    } else if (score < 85) {
        strength = 'strong';
        strengthText = 'Strong';
        warningMessage = '✅ Good! Secure for most purposes.';
    } else {
        strength = 'very-strong';
        strengthText = 'Very Strong';
        warningMessage = '🛡️ Excellent! Highly secure password.';
    }
    
    // Estimate crack time
    const combinations = Math.pow(poolSize, length);
    const crackTime = estimateCrackTime(combinations);
    
    return {
        score: Math.round(score),
        strength: strength,
        strengthText: strengthText,
        warningMessage: warningMessage,
        details: {
            length: length,
            charTypes: charTypes,
            entropy: Math.round(entropy),
            uniqueness: Math.round(uniqueRatio * 100),
            crackTime: crackTime
        }
    };
}

// Estimate time to crack password
function estimateCrackTime(combinations) {
    // Assume 10 billion attempts/second (modern GPU)
    const attemptsPerSecond = 10e9;
    const seconds = combinations / attemptsPerSecond / 2; // Average case
    
    if (seconds < 1) return 'Instant';
    if (seconds < 60) return `${Math.round(seconds)} seconds`;
    if (seconds < 3600) return `${Math.round(seconds / 60)} minutes`;
    if (seconds < 86400) return `${Math.round(seconds / 3600)} hours`;
    if (seconds < 2592000) return `${Math.round(seconds / 86400)} days`;
    if (seconds < 31536000) return `${Math.round(seconds / 2592000)} months`;
    if (seconds < 3153600000) return `${Math.round(seconds / 31536000)} years`;
    return 'Millions of years';
}

// Update strength indicator UI
function updatePasswordStrength(password, options) {
    const result = calculatePasswordStrength(password, options);
    
    // Update text
    const strengthText = document.getElementById('strengthText');
    strengthText.textContent = result.strengthText;
    strengthText.className = 'strength-text ' + result.strength;
    
    // Update bar
    const strengthBar = document.getElementById('strengthBar');
    strengthBar.className = 'strength-bar ' + result.strength;
    
    // Update details with warning message (✅ بدون uniqueness)
    const strengthDetails = document.getElementById('strengthDetails');
    strengthDetails.innerHTML = `
        <div class="strength-warning ${result.strength}">
            ${result.warningMessage}
        </div>
        <div class="strength-metrics">
            <span class="strength-badge ${result.details.length >= 12 ? 'active' : ''}" 
                  title="Password length">
                📏 ${result.details.length} characters
            </span>
            <span class="strength-badge ${result.details.charTypes >= 3 ? 'active' : ''}"
                  title="Number of character types used">
                🎨 ${result.details.charTypes}/4 types
            </span>
            <span class="strength-badge ${result.details.entropy >= 60 ? 'active' : ''}"
                  title="Randomness strength in bits">
                🔐 ${result.details.entropy} bits entropy
            </span>
        </div>
        <div class="strength-crack-time">
            ⏱️ Time to crack: <strong>${result.details.crackTime}</strong>
        </div>
    `;
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
