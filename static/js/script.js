window.command = `bash -c 'curl -L ${window.location.protocol}//${window.location.host}/ | bash'`;

// Set the command text as soon as the page loads
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("cmd").textContent = command;
});

function copyCommand() {
    navigator.clipboard.writeText(command).then(() => {
        const btn = document.querySelector('.copy-btn');
        btn.classList.add('copied');
        btn.innerHTML = '<i class="fas fa-check"></i> Copied!';

        setTimeout(() => {
            btn.classList.remove('copied');
            btn.innerHTML = '<i class="fas fa-copy"></i> Copy';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('failed to copy command. please try manually selecting and copying.');
    });
}

function openLink(url) {
    if (!url) url = atob('aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUXc0dzlXZ1hjUQ=='); // base64

    navigator.clipboard.writeText(url).then(() => {
        console.log('url copied to clipboard');
    }).catch(err => {
        console.error('failed to copy url:', err);
    });

    const aEl = document.createElement('a');
    aEl.style.display = 'none';
    aEl.href = url;
    aEl.target = '_blank';
    aEl.rel = 'noopener';
    document.body.appendChild(aEl);
    aEl.click();
    document.body.removeChild(aEl);
}

function toggleBraveMode() {
    const cmdElement = document.getElementById('cmd');
    const isChecked = document.getElementById('braveToggle').checked;
    if (isChecked) {
        cmdElement.innerHTML = `<span class="shine-red">sudo</span> ${window.command}`;
        window.command = `sudo ${window.command}`;
    } else {
        cmdElement.textContent = cmdElement.textContent.replace(/^sudo\s+/, '');
        window.command = window.command.replace(/^sudo\s+/, '');
    }
}