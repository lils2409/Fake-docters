
    let currentStep = 1;

function showStep(step) {
  // show form step
  document.querySelectorAll('.step').forEach(s => s.classList.add('hidden'));
  document.querySelector(`.step[data-step="${step}"]`).classList.remove('hidden');

  // update vertical stepper
  document.querySelectorAll('.stepper-item').forEach(item => {
    item.classList.remove('active');
    if (Number(item.dataset.step) === step) {
      item.classList.add('active');
    }
  });

  currentStep = step;
}

function nextStep() {
  const current = document.querySelector(`.step[data-step="${currentStep}"]`);
  const inputs = current.querySelectorAll('input, select, textarea');

  for (let input of inputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return;
    }
  }

  showStep(currentStep + 1);
  
}

function prevStep() {
  showStep(currentStep - 1);
}

function updateTriageColor(value) {
  const box = document.getElementById('triageColor');
  const colors = {
    Red: '#ef4444',
    Yellow: '#facc15',
    Green: '#22c55e',
    White: '#e5e7eb',
    Black: '#000000'
  };
  box.style.backgroundColor = colors[value] || '#d1d5db';
}

// Run AFTER page loads
document.addEventListener('DOMContentLoaded', () => {
  showStep(1);
});
function showPage(id, btn){
document.querySelectorAll('.page').forEach(p=>p.classList.add('hidden'));
document.getElementById(id).classList.remove('hidden');
document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('bg-white','shadow'));
btn.classList.add('bg-white','shadow');
}

function updateEditColor(val){
const c={Red:"#F87171",Yellow:"#FACC15",Green:"#4ADE80",White:"#E5E7EB",Black:"#111827"};
document.getElementById("editTriageColor").style.background=c[val]||"#D1D5DB";
}

async function searchPatient(){
const q=document.getElementById("searchEdit").value;
if(q.length<2) return;

const r=await fetch(`/search_patient?q=${q}`);
const d=await r.json();
if(!d) return;

document.getElementById("editForm").classList.remove("hidden");

edit_id.value=d.id;
edit_patient_id.value=d.patient_id;
edit_name.value=d.name;
edit_surname.value=d.surname;
edit_sex.value=d.sex;
edit_age.value=d.age;
edit_height.value=d.height;
edit_weight.value=d.weight;

edit_chronic.value=d.chronic_disease;
edit_allergy.value=d.allergy;
edit_bp.value=d.blood_pressure;
edit_hr.value=d.heart_rate;
edit_bt.value = d.blood_type;
edit_case.value=d.case_desc;
edit_diag.value=d.diagnosis;

edit_color.value=d.color_code;
edit_status.value=d.status;
edit_prescription.value=d.prescription;

updateEditColor(d.color_code);
document.querySelectorAll('#editForm input[name="imaging[]"]').forEach(cb => {
  cb.checked = false;
});

if (d.imaging) {
  const imagingArr = d.imaging.split(",");
  document.querySelectorAll('#editForm input[name="imaging[]"]').forEach(cb => {
    if (imagingArr.includes(cb.value)) {
      cb.checked = true;
    }
  });
}
}

async function saveEdit(){
  const imaging = [];
  document.querySelectorAll('#editForm input[name="imaging[]"]:checked')
    .forEach(cb => imaging.push(cb.value));
await fetch("/update_patient",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
id:edit_id.value,
patient_id:edit_patient_id.value,
name:edit_name.value,
surname:edit_surname.value,
sex:edit_sex.value,
age:edit_age.value,
height:edit_height.value,
weight:edit_weight.value,
chronic_disease:edit_chronic.value,
allergy:edit_allergy.value,
blood_pressure:edit_bp.value,
heart_rate:edit_hr.value,
blood_type: edit_bt.value,
imaging: imaging.join(","),
case_desc:edit_case.value,
diagnosis:edit_diag.value,
color_code:edit_color.value,
prescription:edit_prescription.value
})
});

alert("Patient updated successfully");
}

async function loadStats(){
    const res = await fetch("/stats");
    const data = await res.json();

    document.getElementById("totalPatients").innerText = data.total;
    document.getElementById("waitingPatients").innerText = data.waiting;
    document.getElementById("donePatients").innerText = data.done;

    document.getElementById("redCount").innerText = data.colors.Red;
    document.getElementById("yellowCount").innerText = data.colors.Yellow;
    document.getElementById("greenCount").innerText = data.colors.Green;
    document.getElementById("whiteCount").innerText = data.colors.White;
    document.getElementById("blackCount").innerText = data.colors.Black;
}

// Show Logout Popup
function showLogoutPopup() {
  const modal = document.getElementById("logoutModal");
  modal.classList.remove("hidden");
}

// Close Logout Popup
function closeLogoutPopup() {
  const modal = document.getElementById("logoutModal");
  modal.classList.add("hidden");
}

function logout() {
  window.location.href = "/logout";
}

// Close modal when clicking outside
window.addEventListener("click", (event) => {
  const modal = document.getElementById("logoutModal");
  if (event.target === modal) {
    closeLogoutPopup();
  }
});

async function loadActivePatients() {
  const res = await fetch("/api/active_patients");
  const patients = await res.json();

  const table = document.getElementById("activePatientsTable");
  table.innerHTML = "";

  const triageColors = {
  Red: "#ef4444",
  Yellow: "#facc15",
  Green: "#22c55e",
  White: "#e5e7eb",
  Black: "#000000"
};

  patients.forEach(p => {
    table.innerHTML += `
      <tr class="hover:bg-gray-50 transition">
         <td class="px-6 py-4">
            <div class="w-4 h-4 rounded-full border"
                style="background:${triageColors[p.color] || '#9ca3af'}">
            </div>
          </td>

        <td class="px-6 py-4">${p.patient_id}</td>
        <td class="px-6 py-4">${p.name}</td>
        <td class="px-6 py-4">${p.surname}</td>
        <td class="px-6 py-4">${p.sex}</td>
        <td class="px-6 py-4">${p.age}</td>
        <td class="px-6 py-4">${p.diagnosis || "-"}</td>
        <td class="px-6 py-4">
          <select 
            class="px-3 py-1 rounded-full text-sm font-medium border border-gray-200 bg-white focus:outline-none cursor-pointer"
            onchange="updateStatus(${p.id}, this.value)"
          >
            <option value="Waiting" ${p.status === "Waiting" ? "selected" : ""}>
              Waiting
            </option>
            <option value="Completed" ${p.status === "Completed" ? "selected" : ""}>
              Completed
            </option>
          </select>
        </td>
        <td class="px-6 py-4 flex gap-2">
          <button onclick="deletePatient(${p.id})"
            class="px-3 py-1 text-sm rounded bg-red-500 text-white hover:bg-red-400">
            Delete
          </button>
        </td>
      </tr>
    `;
  });
}

function updateStatus(patientId, newStatus) {
  fetch("/update_patient", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      id: patientId,
      status: newStatus
    })
  })
  .then(res => res.json())
  .then(data => {
    console.log("Status updated");
  });
}


document.addEventListener("DOMContentLoaded", () => {
  showPage("dashboard", document.querySelector(".nav-btn"));
  loadStats();
  loadActivePatients();
});

async function deletePatient(id) {
  if (!confirm("Are you sure you want to delete this patient?")) return;

  const res = await fetch(`/delete_patient/${id}`, {
    method: "DELETE"
  });

  if (res.ok) {
    alert("Patient deleted");
    loadActivePatients(); // refresh table
    loadStats();          // update dashboard numbers
  } else {
    alert("Failed to delete patient");
  }
}

lucide.createIcons();