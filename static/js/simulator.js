(() => {
  const emailTemplate = document.getElementById('emailTemplate');
  const difficultyLevel = document.getElementById('difficultyLevel');
  const targetUsers = document.getElementById('targetUsers');
  const campaignName = document.getElementById('campaignName');
  const campaignDescription = document.getElementById('campaignDescription');
  const createCampaign = document.getElementById('createCampaign');
  const emailPreview = document.getElementById('emailPreview');
  const campaignsList = document.getElementById('campaignsList');
  const totalUsersEl = document.getElementById('totalUsers');
  const totalCampaignsEl = document.getElementById('totalCampaigns');
  const avgClickRateEl = document.getElementById('avgClickRate');
  const validationMsg = document.getElementById('validationMsg');

  let templates = [];
  let users = [];
  let campaigns = [];

  function safeHTML(html) { return html; }

  function selectedUserIds() {
    return Array.from(targetUsers ? targetUsers.selectedOptions : []).map(o => parseInt(o.value, 10)).filter(Number.isFinite);
  }

  function canCreate() {
    const hasTemplate = !!emailTemplate && emailTemplate.value !== '';
    const hasUsers = selectedUserIds().length > 0;
    return hasTemplate && hasUsers;
  }

  function showValidation(msg) {
    if (!validationMsg) return;
    validationMsg.textContent = msg;
    validationMsg.style.display = msg ? 'block' : 'none';
  }

  function updateCreateState() {
    if (!createCampaign) return;
    createCampaign.disabled = !canCreate();
  }

  async function loadTemplates() {
    try {
      const res = await fetch('/api/templates');
      templates = await res.json();
      if (emailTemplate) {
        emailTemplate.innerHTML = '';
        const opt0 = document.createElement('option');
        opt0.value = ''; opt0.textContent = 'Select a template';
        emailTemplate.appendChild(opt0);
        templates.forEach((t, idx) => {
          const opt = document.createElement('option');
          opt.value = String(idx);
          opt.textContent = t.name;
          emailTemplate.appendChild(opt);
        });
        updateCreateState();
      }
    } catch (e) {}
  }

  async function loadUsers() {
    try {
      const res = await fetch('/api/users');
      users = await res.json();
      if (targetUsers) {
        targetUsers.innerHTML = '';
        users.forEach(u => {
          const opt = document.createElement('option');
          opt.value = String(u.id);
          opt.textContent = `${u.name} <${u.email}>`;
          targetUsers.appendChild(opt);
        });
        updateCreateState();
      }
      totalUsersEl && (totalUsersEl.textContent = users.length);
    } catch (e) {}
  }

  async function loadCampaigns() {
    try {
      const res = await fetch('/api/campaigns');
      campaigns = await res.json();
      totalCampaignsEl && (totalCampaignsEl.textContent = campaigns.length);
      renderCampaigns();
      
      let totalClickRate = 0; let counted = 0;
      for (const c of campaigns) {
        const r = await fetch(`/api/analytics/${c.id}`);
        const a = await r.json();
        if (typeof a.click_rate === 'number') { totalClickRate += a.click_rate; counted++; }
      }
      avgClickRateEl && (avgClickRateEl.textContent = (counted ? (totalClickRate / counted).toFixed(1) : '0') + '%');
    } catch (e) {}
  }

  function renderCampaigns() {
    if (!campaignsList) return;
    campaignsList.innerHTML = '';
    if (!Array.isArray(campaigns) || campaigns.length === 0) return;
    campaigns.forEach(c => {
      const card = document.createElement('div');
      card.className = 'campaign-card';
      card.innerHTML = `
        <div class="title">${c.name}</div>
        <div class="meta">${c.description || ''}</div>
        <div class="meta">Template: ${c.email_template} • Difficulty: ${c.difficulty_level} • Attack: ${c.attack_type}</div>
        <div class="meta">Status: ${c.status} • Recipients: ${c.recipient_count}</div>
        <div class="footer">
          <button class="btn" data-action="send">Send</button>
          <button class="btn" data-action="recipients">Recipients</button>
          <button class="btn" data-action="analytics">Analytics</button>
        </div>
      `;
      card.querySelector('[data-action="send"]').addEventListener('click', async () => {
        try {
          await fetch(`/api/send-campaign/${c.id}`, { method: 'POST' });
          await loadCampaigns();
        } catch (e) {}
      });
      card.querySelector('[data-action="analytics"]').addEventListener('click', () => {
        window.location.href = '/analytics';
      });
      card.querySelector('[data-action="recipients"]').addEventListener('click', async () => {
        await showRecipientsModal(c.id, c.name);
      });
      campaignsList.appendChild(card);
    });
  }

  function updatePreview() {
    if (!emailPreview || !emailTemplate) return;
    const idx = parseInt(emailTemplate.value, 10);
    const t = Number.isFinite(idx) ? templates[idx] : null;
    if (!t) {
      emailPreview.innerHTML = `
        <div class="preview-placeholder">
          <i class="fas fa-envelope"></i>
          <p>Select an email template to preview</p>
        </div>
      `;
      return;
    }
    emailPreview.innerHTML = `<div class="preview-html">${safeHTML(t.content)}</div>`;
  }

  async function onCreateCampaign() {
    const idx = parseInt(emailTemplate.value, 10);
    const tpl = Number.isFinite(idx) ? templates[idx] : null;
    const selectedUsers = selectedUserIds();
    if (!tpl || selectedUsers.length === 0) {
      showValidation('Please select an email template and at least one user.');
      return;
    }
    showValidation('');
    if (createCampaign) { createCampaign.disabled = true; createCampaign.textContent = 'Creating...'; }
    const payload = {
      name: campaignName && campaignName.value ? campaignName.value : `Campaign ${Date.now()}`,
      description: campaignDescription ? campaignDescription.value : '',
      email_template: tpl.name,
      subject_line: tpl.subject || tpl.name,
      sender_name: tpl.sender_name,
      sender_email: tpl.sender_email,
      difficulty_level: difficultyLevel ? difficultyLevel.value : (tpl.difficulty || 'easy'),
      attack_type: tpl.attack_vector,
      recipients: selectedUsers
    };
    try {
      await fetch('/api/campaigns', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      await loadCampaigns();
      if (campaignName) campaignName.value = '';
      if (campaignDescription) campaignDescription.value = '';
      if (emailTemplate) emailTemplate.value = '';
      if (targetUsers) Array.from(targetUsers.options).forEach(o => o.selected = false);
      updateCreateState();
      showValidation('Campaign created successfully!');
    } catch (e) {
      showValidation('Error creating campaign. Please try again.');
    }
    if (createCampaign) { createCampaign.disabled = false; createCampaign.textContent = 'Create Campaign'; }
  }

  async function showRecipientsModal(campaignId, campaignName){
    try{
      const res = await fetch(`/api/campaign-recipients/${campaignId}`);
      const list = await res.json();
      const modal = document.getElementById('campaignModal');
      const details = document.getElementById('campaignDetails');
      if(!modal || !details) return;
      const rows = (list || []).map(r => `
        <tr>
          <td>${r.id}</td>
          <td>${r.name}</td>
          <td>${r.email}</td>
          <td>${r.email_sent ? 'Yes' : 'No'}</td>
          <td>${r.email_opened ? 'Yes' : 'No'}</td>
          <td>${r.link_clicked ? 'Yes' : 'No'}</td>
          <td>${r.credentials_submitted ? 'Yes' : 'No'}</td>
          <td>
            <button class="btn" data-sim="open" data-user="${r.id}">Open</button>
            <button class="btn" data-sim="click" data-user="${r.id}">Click</button>
          </td>
        </tr>`).join('');
      details.innerHTML = `
        <h3>${campaignName}</h3>
        <table class="table">
          <thead>
            <tr>
              <th>ID</th><th>Name</th><th>Email</th><th>Sent</th><th>Opened</th><th>Clicked</th><th>Creds</th><th>Simulate</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>`;
      modal.style.display = 'block';
      document.body.style.overflow = 'hidden';
      details.querySelectorAll('[data-sim="open"]').forEach(btn => {
        btn.addEventListener('click', async () => {
          const userId = btn.getAttribute('data-user');
          await fetch(`/track/open/${campaignId}/${userId}`);
          await showRecipientsModal(campaignId, campaignName);
        });
      });
      details.querySelectorAll('[data-sim="click"]').forEach(btn => {
        btn.addEventListener('click', () => {
          const userId = btn.getAttribute('data-user');
          window.open(`/phishing/${campaignId}/${userId}`, '_blank');
        });
      });
      const close = document.querySelector('#campaignModal .close');
      if(close){ close.onclick = () => { modal.style.display = 'none'; document.body.style.overflow='auto'; } }
      modal.onclick = (e) => { if(e.target === modal){ modal.style.display = 'none'; document.body.style.overflow='auto'; } };
    }catch(e){}
  }

  window.showTemplateManager = function() { alert('Template Manager coming soon'); };
  window.showUserManager = function() { window.location.href = '/admin'; };
  window.showAnalytics = function() { window.location.href = '/analytics'; };
  window.showTraining = function() { alert('Training mode coming soon'); };

  emailTemplate && emailTemplate.addEventListener('change', () => { updatePreview(); updateCreateState(); });
  targetUsers && targetUsers.addEventListener('change', updateCreateState);
  createCampaign && createCampaign.addEventListener('click', onCreateCampaign);

  const addDemoUsers = document.getElementById('addDemoUsers');
  if(addDemoUsers){
    addDemoUsers.addEventListener('click', async () => {
      await fetch('/api/seed-users', { method: 'POST' });
      await loadUsers();
    });
  }

  loadTemplates().then(updatePreview);
  loadUsers();
  loadCampaigns();
  updateCreateState();
})();