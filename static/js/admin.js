(() => {
  const userName = document.getElementById('userName');
  const userEmail = document.getElementById('userEmail');
  const userDepartment = document.getElementById('userDepartment');
  const userRole = document.getElementById('userRole');
  const addUserBtn = document.getElementById('addUserBtn');
  const usersTableBody = document.querySelector('#usersTable tbody');
  const adminCampaigns = document.getElementById('adminCampaigns');
  const adminTemplates = document.getElementById('adminTemplates');

  async function loadUsers(){
    try{
      const res = await fetch('/api/users');
      const users = await res.json();
      usersTableBody.innerHTML = '';
      users.forEach(u=>{
        const tr = document.createElement('tr');
        [u.id, u.name, u.email, u.department || '', u.role || '', u.created_at].forEach(v=>{
          const td = document.createElement('td'); td.textContent = v; tr.appendChild(td);
        });
        usersTableBody.appendChild(tr);
      });
    }catch(e){}
  }

  async function addUser(){
    const name = userName.value.trim();
    const email = userEmail.value.trim();
    const department = userDepartment.value.trim();
    const role = userRole.value.trim();
    if(!name || !email) return;
    try{
      await fetch('/api/users',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ name, email, department, role })
      });
      userName.value=''; userEmail.value=''; userDepartment.value=''; userRole.value='';
      await loadUsers();
    }catch(e){}
  }

  async function loadCampaigns(){
    try{
      const res = await fetch('/api/campaigns');
      const campaigns = await res.json();
      adminCampaigns.innerHTML = '';
      campaigns.forEach(c=>{
        const card = document.createElement('div');
        card.className = 'campaign-card';
        card.innerHTML = `
          <div class="title">${c.name}</div>
          <div class="meta">${c.description || ''}</div>
          <div class="meta">Template: ${c.email_template} • Difficulty: ${c.difficulty_level} • Attack: ${c.attack_type}</div>
          <div class="meta">Status: ${c.status} • Recipients: ${c.recipient_count}</div>
          <div class="footer">
            <button class="btn" data-action="send">Send</button>
            <button class="btn" data-action="analytics">Analytics</button>
          </div>
        `;
        card.querySelector('[data-action="send"]').addEventListener('click', async ()=>{
          try{ await fetch(`/api/send-campaign/${c.id}`,{method:'POST'}); await loadCampaigns(); }catch(e){}
        });
        card.querySelector('[data-action="analytics"]').addEventListener('click', ()=>{ window.location.href = '/analytics'; });
        adminCampaigns.appendChild(card);
      });
    }catch(e){}
  }

  async function loadTemplates(){
    try{
      const res = await fetch('/api/templates');
      const templates = await res.json();
      adminTemplates.innerHTML = '';
      templates.forEach(t=>{
        const card = document.createElement('div');
        card.className = 'campaign-card';
        card.innerHTML = `
          <div class="title">${t.name}</div>
          <div class="meta">Category: ${t.category} • Difficulty: ${t.difficulty}</div>
          <div class="meta">Sender: ${t.sender_name} <${t.sender_email}></div>
          <div class="meta">Attack: ${t.attack_vector}</div>
        `;
        adminTemplates.appendChild(card);
      });
    }catch(e){}
  }

  addUserBtn && addUserBtn.addEventListener('click', addUser);

  loadUsers();
  loadCampaigns();
  loadTemplates();
})();