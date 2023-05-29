<center>
  <div class="text-center" style="width: 80%;">
    <h1>Troca na Escola 📚</h1>

    <p>Juntos pelo aprendizado dos nossos pequenos.</p>

    <!-- <p>- Doe ou busque seu livro de interesse</p> -->
    <div class="topnav mt-3">
      <input type="text" placeholder="Escreva o título do livro" style="width: 305px; font-size: 14px;">
      <!-- <input type="text" placeholder="Escreva o título do livro" style="width: 305px;"> -->
      <button type="button" class="btn btn-outline-primary">Buscar  🔎 </button>
    </div>
  </div>
  <div class="text-center">
  <p style="display: inline-block; margin-right: 10px;"><span style="font-size: 1rem;">Tem algum livro didático para doação?</span></p>
  <button type="button" class="btn btn-primary" onclick="window.location.href='/donate'">Quero doar 👍</button>
</div>

  <table class="card-table table">
    <thead id="search-header">
      <tr>
        <th scope="col"><center>Livro</center></th>
        <th scope="col"><center></center></th>
      </tr>
    </thead>
    <tbody id="search-results">
      <!-- Search results will be appended here -->
    </tbody>
  </table>
</div>

</center>
<center><div class="card" style="width: 40rem;"></center>
  <div class="card-header">
    <center><h4><br>O livro que você procura pode estar aqui!</h4></center>
    <center><p>Faça sua busca pelo título do livro.<br>Encontrou um doador disponível?<br>Clique em "Tenho Interesse" para combinar a troca com o doador.<br><br>Vamos nessa? 📚</p></center>
  </div>

<script>
// Determine the base URL depending on the environment (production or development)
var BASE_URL = '';
if (window.location.hostname === "localhost" || window.location.hostname === "0.0.0.0") {
    BASE_URL = 'http://0.0.0.0:5001';
} else {
    BASE_URL = 'https://be-troca-na-escola.herokuapp.com';
}

function hideSearchCard() {
    const searchCard = document.querySelector('.card');
    const searchHeader = document.querySelector('#search-header');
    searchCard.style.display = 'none';
    searchHeader.style.display = 'none';
}

hideSearchCard();

async function sendEmail(donationId) {
    // Fetch donation details
    const donationResponse = await fetch(`${BASE_URL}/api/donations?donation_id=${donationId}`);
    const donationData = await donationResponse.json();
    const userId = donationData.data[0].relationships.owner.id;
    const bookName = donationData.data[0].attributes.name;

    // Fetch user details
    const userResponse = await fetch(`${BASE_URL}/api/users?user_id=${userId}`);
    const userData = await userResponse.json();
    const recipient_email = userData.data[0].attributes.email;
    const recipient_name = userData.data[0].attributes.name;

    // Collect person's name and email
    const person_name = prompt("Por favor digite seu nome de contato:");
    const person_contact = prompt("Por favor, entre com seu contato (email ou celular):");

    // Send email
    const response = await fetch("/send-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            recipient_email: recipient_email,
            message: `Olá "${recipient_name}",  ${person_name}  com o contato (email ou celular): ${person_contact} está interessado no livro: "${bookName}". Basta agora entrar em contato com essa pessoa para vocês combinarem a troca! Boa troca - \n\n Time Troca Na Escola`,
        }),
    });

    if (response.ok) {
        alert("Email enviado! Agora é só aguardar o retorno da pessoa doadora :)");
    } else {
        alert("Failed to send email.");
    }
}

function performSearch() {
    document.querySelector('.card').style.display = 'block';
    document.querySelector('#search-header').style.display = 'table-header-group';

    async function fetchData() {
        const query = document.querySelector('input[type="text"]').value;
        const response = await fetch(`${BASE_URL}/api/donations?name=${query}`);
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
            button.textContent = "Tenho interesse✨";
            button.className = "btn btn-primary";
            button.onclick = () => sendEmail(result.id);
            
            const centerElement = document.createElement('center');
            centerElement.appendChild(button);
            //emailBtn.appendChild(button);
            emailBtn.appendChild(centerElement);

            name.innerHTML = `<center>${result.attributes.name}</center>`;
            //userid.innerHTML = `<center><a href="#" onclick="sendEmail('${result.relationships.owner.email}')">${result.relationships.owner.id}</a></center>`;
            userid.innerHTML = `<center>${result.relationships.owner.id}</center>`;

            row.appendChild(name);
            //row.appendChild(userid);
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

