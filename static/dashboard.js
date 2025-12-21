// Fetch dashboard data from backend
fetch("/dashboard-data")
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById("table-body");

        // Clear old data
        tableBody.innerHTML = "";

        data.forEach(item => {
            const row = document.createElement("tr");

            // Name, Email, College
            const nameCell = document.createElement("td");
            nameCell.innerText = item.name;
            row.appendChild(nameCell);

            const emailCell = document.createElement("td");
            emailCell.innerText = item.email;
            row.appendChild(emailCell);

            const collegeCell = document.createElement("td");
            collegeCell.innerText = item.college;
            row.appendChild(collegeCell);

            // Skills as badges
            const skillsCell = document.createElement("td");
            item.skills.forEach(skill => {
                const badge = document.createElement("span");
                badge.className = "skill-badge";
                badge.innerText = skill;
                skillsCell.appendChild(badge);
            });
            row.appendChild(skillsCell);

            // Match Score
            const scoreCell = document.createElement("td");
            scoreCell.innerText = item.match_score + "%";
            row.appendChild(scoreCell);

            // Date
            const dateCell = document.createElement("td");
            const dateObj = new Date(item.created_at);
            dateCell.innerText = dateObj.toLocaleString();
            row.appendChild(dateCell);

            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error("Error fetching dashboard data:", error);
    });