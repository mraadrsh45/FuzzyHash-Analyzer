// FUZZYHASH ANALYZER - DUAL FILE UPLOAD & ANALYSIS PIPELINE JS

document.addEventListener('DOMContentLoaded', () => {
    setupDropzone('dropzone-a', 'input-a', 'info-a');
    setupDropzone('dropzone-b', 'input-b', 'info-b');

    const form = document.getElementById('analysis-form');
    const btnSubmit = document.getElementById('btn-submit-analysis');
    const progressOverlay = document.getElementById('analysis-progress-overlay');
    const progressStepText = document.getElementById('progress-step-text');
    const progressBarFill = document.getElementById('progress-bar-fill');

    function checkReady() {
        const fileA = document.getElementById('input-a').files[0];
        const fileB = document.getElementById('input-b').files[0];
        const caseSelect = document.getElementById('case_id');

        if (fileA && fileB && caseSelect.value) {
            btnSubmit.disabled = false;
        } else {
            btnSubmit.disabled = true;
        }
    }

    document.getElementById('case_id')?.addEventListener('change', checkReady);

    function setupDropzone(zoneId, inputId, infoId) {
        const zone = document.getElementById(zoneId);
        const input = document.getElementById(inputId);
        const info = document.getElementById(infoId);

        if (!zone || !input || !info) return;

        zone.addEventListener('click', () => input.click());

        zone.addEventListener('dragover', (e) => {
            e.preventDefault();
            zone.classList.add('dragover');
        });

        zone.addEventListener('dragleave', () => {
            zone.classList.remove('dragover');
        });

        zone.addEventListener('drop', (e) => {
            e.preventDefault();
            zone.classList.remove('dragover');
            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                input.files = e.dataTransfer.files;
                updateFileInfo(input.files[0], info);
                checkReady();
            }
        });

        input.addEventListener('change', () => {
            if (input.files && input.files.length > 0) {
                updateFileInfo(input.files[0], info);
                checkReady();
            }
        });
    }

    function updateFileInfo(file, infoEl) {
        if (!file) return;
        const sizeFormatted = formatBytes(file.size);
        const typeStr = file.type || 'Binary / Raw Data';

        infoEl.style.display = 'block';
        infoEl.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <strong style="color: var(--accent-cyan);">${escapeHtml(file.name)}</strong>
                    <div style="font-size: 11px; color: var(--text-muted);">${sizeFormatted} | ${escapeHtml(typeStr)}</div>
                </div>
                <span style="color: var(--accent-emerald); font-weight: bold;">✓ Ready</span>
            </div>
        `;
    }

    function formatBytes(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1048576) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / 1048576).toFixed(2) + ' MB';
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    // Step-by-step progress simulation on form submit
    if (form) {
        form.addEventListener('submit', (e) => {
            if (progressOverlay) {
                progressOverlay.style.display = 'flex';
            }

            const steps = [
                { text: 'File Validation & Path Security Check...', pct: 15 },
                { text: 'Extracting Structural Metadata...', pct: 30 },
                { text: 'Calculating MD5 & SHA-256 Hashes...', pct: 50 },
                { text: 'Generating ssdeep CTPH & TLSH Fuzzy Hashes...', pct: 70 },
                { text: 'Comparing Structural Fuzzy Hash Distance...', pct: 85 },
                { text: 'Generating Forensic PDF Report...', pct: 95 },
                { text: 'Analysis Pipeline Complete.', pct: 100 }
            ];

            let stepIdx = 0;
            const interval = setInterval(() => {
                if (stepIdx < steps.length) {
                    if (progressStepText) progressStepText.innerText = steps[stepIdx].text;
                    if (progressBarFill) progressBarFill.style.width = steps[stepIdx].pct + '%';
                    stepIdx++;
                } else {
                    clearInterval(interval);
                }
            }, 300);
        });
    }
});
