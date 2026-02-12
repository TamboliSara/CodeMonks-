document.getElementById('productForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const verifyBtn = document.getElementById('verifyBtn');
    verifyBtn.innerText = "Verifying on Blockchain...";
    verifyBtn.disabled = true;

    // Gather Data
    const formData = {
        product_name: document.getElementById('product_name').value,
        claims: document.getElementById('claims').value,
        net_quantity: document.getElementById('net_quantity').value,
        mrp: document.getElementById('mrp').value,
        batch_number: document.getElementById('batch_number').value,
        expiry_date: document.getElementById('expiry_date').value,
        manufacturer_details: document.getElementById('manufacturer').value,
        consumer_care_contact: document.getElementById('customer_care').value
    };

    try {
        const response = await fetch('/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        alert("Verification failed. Check console.");
    } finally {
        verifyBtn.innerText = "Verify Compliance";
        verifyBtn.disabled = false;
    }
});

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.classList.remove('hidden');

    const compliance = data.compliance;
    
    // Set Badge and Score
    const badge = document.getElementById('badge');
    badge.innerText = compliance.status;
    badge.className = `badge ${compliance.status}`;
    
    document.getElementById('trustScore').innerText = compliance.final_score;
    
    // Metrology details
    const metrologyStatus = document.getElementById('metrologyStatus');
    if (compliance.metrology_check.missing.length > 0) {
        metrologyStatus.innerHTML = `<span style="color:red">Missing: ${compliance.metrology_check.missing.join(', ')}</span>`;
    } else {
        metrologyStatus.innerHTML = `<span style="color:green">✔ All Mandatory Fields Present</span>`;
    }

    // Claim Issues
    const issuesList = document.getElementById('claimIssues');
    issuesList.innerHTML = "";
    if (compliance.claim_issues.length === 0) {
        issuesList.innerHTML = "<li>✔ No misleading claims detected.</li>";
    } else {
        compliance.claim_issues.forEach(issue => {
            const li = document.createElement('li');
            li.style.color = issue.type === "HARD_FAIL" ? "red" : "orange";
            li.innerText = `[${issue.type}] ${issue.message}`;
            issuesList.appendChild(li);
        });
    }

    // Blockchain TxID
    document.getElementById('txId').innerText = data.blockchain_tx_id;
}
