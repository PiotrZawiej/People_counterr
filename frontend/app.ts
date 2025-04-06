document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form") as HTMLFormElement;
    const fileInput = document.getElementById("image-upload") as HTMLInputElement;
    const responseDiv = document.getElementById("upload-response") as HTMLDivElement;

    uploadForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        if (!fileInput.files || fileInput.files.length === 0) {
            responseDiv.textContent = "Please select a file before submitting.";
            return;
        }

        const formData = new FormData();
        formData.append("file", fileInput.files[0]);

        try {
            const res = await fetch("http://localhost:8000/upload_image", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                throw new Error("An error occurred while uploading the file.");
            }

            const data = await res.json();
            responseDiv.innerHTML = `
                <strong>Image successfully sent for processing!</strong><br>
                <strong>Event ID:</strong> <code>${data.eventid}</code><br>
                <strong>Status:</strong> ${data.status}
            `;
        } catch (err) {
            if (err instanceof Error) {
                responseDiv.textContent = "Error: " + err.message;
            } else {
                responseDiv.textContent = "An unknown error occurred.";
            }
        }
    });
});
