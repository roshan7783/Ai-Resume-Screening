const form = document.getElementById("resumeForm");
const loader = document.getElementById("loader");
const resultBox = document.getElementById("result");
const skillsText = document.getElementById("skills");
const scoreText = document.getElementById("score");

const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const college = document.getElementById("college").value.trim();
    const jobDesc = document.getElementById("jobDesc").value.trim();
    const resumeInput = document.getElementById("resume");
    const resumeFile = resumeInput.files[0];

    // Frontend validation
    if (!name || !email || !college || !jobDesc || !resumeFile) {
        alert("⚠️ Please fill all required fields before analyzing.");
        return;
    }

    // Reset UI
    resultBox.style.display = "none";
    loader.style.display = "block";
    progressContainer.style.display = "block";
    progressBar.style.width = "0%";
    skillsText.innerHTML = "";

    // Fake progress animation
    let progress = 0;
    const interval = setInterval(() => {
        if (progress < 90) {
            progress += 10;
            progressBar.style.width = progress + "%";
        }
    }, 300);

    // ✅ IMPORTANT: Manually append form data
    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);
    formData.append("college", college);
    formData.append("job", jobDesc);          // MUST be "job"
    formData.append("resume", resumeFile);    // MUST be "resume"

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        clearInterval(interval);
        progressBar.style.width = "100%";
        loader.style.display = "none";

        if (!response.ok) {
            alert(data.error || "Server error");
            return;
        }

        // Show result
        resultBox.style.display = "block";
        scoreText.innerText = data.match_score + " %";

        // Skill badges
        data.skills_found.forEach(skill => {
            const badge = document.createElement("span");
            badge.className = "skill-badge";
            badge.innerText = skill;
            skillsText.appendChild(badge);
        });

    } catch (error) {
        clearInterval(interval);
        loader.style.display = "none";
        alert("❌ Something went wrong. Please try again.");
        console.error(error);
    }
});