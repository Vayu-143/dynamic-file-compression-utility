// ==========================================
// Load Statistics
// ==========================================

async function loadStatistics() {

    let stats =
        await fetch(
            "/statistics"
        );

    stats =
        await stats.json();

    document.getElementById(
        "total"
    ).innerText =
        stats.total_compressions;

    document.getElementById(
        "decompressions"
    ).innerText =
        stats.total_decompressions;

    document.getElementById(
        "ratio"
    ).innerText =
        stats.average_ratio + "%";

    document.getElementById(
        "time"
    ).innerText =
        stats.average_execution_time;
}


// ==========================================
// Load Compression History
// ==========================================

async function loadHistory() {

    let response =
        await fetch(
            "/history"
        );

    let data =
        await response.json();

    let html = "";

    data.history.forEach(
        item => {

            html += `
            <tr>

                <td>${item.id}</td>

                <td>${item.operation}</td>

                <td>${item.filename}</td>

                <td>${item.original_size}</td>

                <td>${item.compressed_size}</td>

                <td>${item.ratio}%</td>

                <td>
                    <button
                        class="btn btn-danger btn-sm"
                        onclick="deleteRecord(${item.id})"
                    >
                        Delete
                    </button>
                </td>

            </tr>
            `;
        }
    );

    document.getElementById(
        "historyTable"
    ).innerHTML =
        html;
}


// ==========================================
// Delete Single Record
// ==========================================

async function deleteRecord(id) {

    if (
        !confirm(
            "Delete this history record?"
        )
    ) {
        return;
    }

    await fetch(
        `/history/${id}`,
        {
            method: "DELETE"
        }
    );

    loadHistory();
    loadStatistics();
}


// ==========================================
// Clear All History
// ==========================================

async function clearHistory() {

    if (
        !confirm(
            "Delete all history?"
        )
    ) {
        return;
    }

    await fetch(
        "/history",
        {
            method: "DELETE"
        }
    );

    loadHistory();
    loadStatistics();
}


// ==========================================
// Compress File
// ==========================================

async function compressFile() {

    const file =
        document.getElementById(
            "compressFile"
        ).files[0];

    if (!file) {

        alert(
            "Please select a file."
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await fetch(
            "/compress",
            {
                method: "POST",
                body: formData
            }
        );

    const data =
        await response.json();

    document.getElementById(
        "compressResult"
    ).innerHTML =
    `
    <div class="alert alert-success">

        File Compressed Successfully

    </div>
    `;

    loadStatistics();
    loadHistory();
}


// ==========================================
// Decompress File
// ==========================================

async function decompressFile() {

    const binaryFile =
        document.getElementById(
            "binaryFile"
        ).files[0];

    const metadataFile =
        document.getElementById(
            "metadataFile"
        ).files[0];

    if (
        !binaryFile ||
        !metadataFile
    ) {

        alert(
            "Select both files."
        );

        return;
    }

    const formData =
        new FormData();

    formData.append(
        "binary_file",
        binaryFile
    );

    formData.append(
        "metadata_file",
        metadataFile
    );

    const response =
        await fetch(
            "/decompress",
            {
                method: "POST",
                body: formData
            }
        );

    const data =
        await response.json();

    document.getElementById(
        "decompressResult"
    ).innerHTML =
    `
    <div class="alert alert-info">

        File Restored Successfully

    </div>
    `;

    loadStatistics();
    loadHistory();
}


// ==========================================
// Auto Refresh Dashboard
// ==========================================

loadStatistics();
loadHistory();

setInterval(
    loadStatistics,
    3000
);

setInterval(
    loadHistory,
    3000
);