(function(){
  var projectModal = document.getElementById('projectModal');
  var modalTitle = document.getElementById('modalTitle');
  var modalDescription = document.getElementById('modalDescription');
  var modalFeatures = document.getElementById('modalFeatures');
  var modalSkills = document.getElementById('modalSkills');
  var modalOutcomes = document.getElementById('modalOutcomes');
  var modalScreenshots = document.getElementById('modalScreenshots');
  var modalSpecs = document.getElementById('modalSpecs');
  var modalClose = document.querySelector('.modal-close');
  var hamburger = document.querySelector('.hamburger');
  var navMenu = document.querySelector('.nav-menu');

  var projectData = {
    phishing: {
      title: 'Phishing Email Simulation',
      description: 'Advanced simulation platform to train employees to recognize email-based attacks.',
      features: [
        'Realistic email templates',
        'Interactive training with feedback',
        'Analytics dashboard with metrics'
      ],
      skills: ['Flask','Python','SQLite','HTML5','CSS3','JavaScript','Jinja2'],
      outcomes: [
        'Improved phishing recognition',
        'Reduced successful attacks',
        'Measured engagement and awareness'
      ],
      specs: 'Flask backend with SQLite storage, responsive UI with HTML/CSS, dynamic JS interactions.'
    },
    training: {
      title: 'Security Awareness Training',
      description: 'Interactive modules, quizzes, and certification workflows for teams.',
      features: [
        'Role-based modules',
        'Progress tracking',
        'Certification'
      ],
      skills: ['React','Node.js','MongoDB','JWT'],
      outcomes: ['Higher awareness','Better compliance','Reduced incidents'],
      specs: 'Modular architecture with modern web stack and secure auth.'
    },
    vulnerability: {
      title: 'Vulnerability Assessment Tool',
      description: 'Automated scanning to identify misconfigurations and risks.',
      features: ['Network scans','Config checks','Risk scoring'],
      skills: ['Python','Nmap','PostgreSQL','Docker'],
      outcomes: ['Fewer misconfigurations','Faster remediation','Improved posture'],
      specs: 'Automated scanning workflows with reporting and exports.'
    }
  };

  function openModal(key){
    var p = projectData[key];
    if(!p || !projectModal) return;
    if(modalTitle) modalTitle.textContent = p.title;
    if(modalDescription) modalDescription.textContent = p.description;
    if(modalFeatures) modalFeatures.innerHTML = p.features.map(function(f){ return '<li>'+f+'</li>'; }).join('');
    if(modalSkills) modalSkills.innerHTML = p.skills.map(function(s){ return '<span class="tech-badge">'+s+'</span>'; }).join('');
    if(modalOutcomes) modalOutcomes.innerHTML = p.outcomes.map(function(o){ return '<li>'+o+'</li>'; }).join('');
    if(modalScreenshots) modalScreenshots.innerHTML = [
      'Main Dashboard','Analytics View','Settings Panel','Mobile Interface'
    ].map(function(t){ return '<div class="screenshot-placeholder">'+t+'</div>'; }).join('');
    if(modalSpecs) modalSpecs.innerHTML = '<h4>Technical Architecture</h4><p>'+p.specs+'</p>';
    projectModal.style.display = 'block';
    document.body.style.overflow = 'hidden';
  }

  function closeModal(){
    if(!projectModal) return;
    projectModal.style.display = 'none';
    document.body.style.overflow = 'auto';
  }

  var buttons = document.querySelectorAll('.demo-btn, .details-btn');
  for(var i=0;i<buttons.length;i++){
    buttons[i].addEventListener('click', function(e){
      e.preventDefault();
      var key = this.getAttribute('data-project');
      openModal(key);
    });
  }

  if(modalClose){ modalClose.addEventListener('click', closeModal); }
  if(projectModal){
    projectModal.addEventListener('click', function(e){ if(e.target === projectModal) closeModal(); });
  }
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && projectModal && projectModal.style.display === 'block'){ closeModal(); } });

  if(hamburger && navMenu){
    hamburger.addEventListener('click', function(){ navMenu.classList.toggle('open'); });
  }
})();