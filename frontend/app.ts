document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form") as HTMLFormElement;
    const fileInput = document.getElementById("image-upload") as HTMLInputElement;
    const responseDiv = document.getElementById("upload-response") as HTMLDivElement;
    const processedImage = document.getElementById("processed-image") as HTMLImageElement;

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
            const eventID = data.eventid;

            console.log(eventID)

            responseDiv.innerHTML = `
                <strong>Image sent successfully!</strong><br>
                Processing... Please wait.
            `;

            // 🔁 Poll backend for result
            const interval = setInterval(async () => {
                const res = await fetch(`http://localhost:8000/get_result?eventid=${eventID}`);
                const resultData = await res.json();

                if (resultData.result?.status === "completed") {
                    clearInterval(interval);
                    const count = resultData.result.human_count;
                    const imageUrl = resultData.result.image_url;

                    responseDiv.innerHTML = `
                        Detection complete!<br>
                        People detected: <strong>${count}</strong>
                    `;

                    processedImage.src = imageUrl;
                    processedImage.style.display = "block";
                }
            }, 2000);

        } catch (err) {
            if (err instanceof Error) {
                responseDiv.textContent = "Error: " + err.message;
            } else {
                responseDiv.textContent = "An unknown error occurred.";
            }
        }
    });
});
