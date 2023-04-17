<h1>Bem-vinde ao QueroLer 📚</h1>

Doador 🤝 Quem quer ler

- Doe ou busque seu livro de interesse

<button type="button" class="btn btn-primary">QueroDoar</button>

<div class="topnav">
  <input type="text" placeholder="Buscar 🔎 ">
  <button type="button" class="btn btn-outline-primary">search</button>
</div>
<center><div class="card" style="width: 40rem;"></center>
  <div class="card-header">
    <center><h5>Livraria solidária disponível</h5></center>
  </div>
  <table class="card-table table">
    <thead id="search-header">
      <tr>
        <th scope="col"><center>Título</center></th>
        <th scope="col"><center>user_id 🔗 </center></th>
        <th scope="col"><center>Email</center></th>
      </tr>
    </thead>
    <tbody id="search-results">
      <!-- Search results will be appended here -->
    </tbody>
  </table>
</div>

<script>
function hideSearchCard() {
    const searchCard = document.querySelector('.card');
    const searchHeader = document.querySelector('#search-header');
    searchCard.style.display = 'none';
    searchHeader.style.display = 'none';
}

hideSearchCard();

async function sendEmail(donationId) {
    // Fetch donation details
    const donationResponse = await fetch(`http://0.0.0.0:5001/api/donations?donation_id=${donationId}`);
    const donationData = await donationResponse.json();
    const userId = donationData.data[0].relationships.owner.id;

    // Fetch user details
    const userResponse = await fetch(`http://0.0.0.0:5001/api/users?user_id=${userId}`);
    const userData = await userResponse.json();
    const recipient_email = userData.data[0].attributes.email;

    // Collect person's name and email
    const person_name = prompt("Please enter your name:");
    const person_email = prompt("Please enter your email:");

    // Send email
    const response = await fetch("/send-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            recipient_email: recipient_email,
            message: `Here is your personalized message from QueroLer! The person ${person_name} with email ${person_email} pressed the Email button and is interested in your book.`,
        }),
    });

    if (response.ok) {
        alert("Email sent!");
    } else {
        alert("Failed to send email.");
    }
}

function performSearch() {
    document.querySelector('.card').style.display = 'block';
    document.querySelector('#search-header').style.display = 'table-header-group';

    async function fetchData() {
        const query = document.querySelector('input[type="text"]').value;
        const response = await fetch(`http://0.0.0.0:5001/api/donations?name=${query}`);
        const results = await response.json();
        const tableBody = document.querySelector('#search-results');
        tableBody.innerHTML = '';

        results.data.forEach(result => {
            const row = document.createElement('tr');
            const name = document.createElement('td');
            const userid = document.createElement('td');

            // Move the emailBtn creation here
            const emailBtn = document.createElement('td');
            const button = document.createElement('button');
            button.textContent = "Email";
            button.className = "btn btn-primary";
            button.onclick = () => sendEmail(result.id);
            emailBtn.appendChild(button);

            name.innerHTML = `<center>${result.attributes.name}</center>`;
            //userid.innerHTML = `<center><a href="#" onclick="sendEmail('${result.relationships.owner.email}')">${result.relationships.owner.id}</a></center>`;
            userid.innerHTML = `<center>${result.relationships.owner.id}</center>`;

            row.appendChild(name);
            row.appendChild(userid);
            row.appendChild(emailBtn); // Add the email button to the row
            tableBody.appendChild(row);
        });
    }

    fetchData();
}

document.querySelector('.btn-outline-primary').addEventListener('click', performSearch);
document.querySelector('input[type="text"]').addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        performSearch();
    }
});
</script>
