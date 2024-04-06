const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');

const darkMode = document.querySelector('.dark-mode');

menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
});

darkMode.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode-variables');
    darkMode.querySelector('span:nth-child(1)').classList.toggle('active');
    darkMode.querySelector('span:nth-child(2)').classList.toggle('active');
})


Orders.forEach(order => {
    const tr = document.createElement('tr');
    const trContent = `
        <td>${order.productName}</td>
        <td>${order.productNumber}</td>
        <td>${order.paymentStatus}</td>
        <td class="${order.status === 'Declined' ? 'danger' : order.status === 'Pending' ? 'warning' : 'primary'}">${order.status}</td>
        <td class="primary">Details</td>
    `;
    tr.innerHTML = trContent;
    document.querySelector('table tbody').appendChild(tr);
});

//search
function searchTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.querySelector(".recent-orders table");
    tr = table.getElementsByTagName("tr");

    
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; 
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function searchTabel() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.querySelector(".data table");
    tr = table.getElementsByTagName("tr");

    
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; 
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// Fungsi untuk menampilkan lebih banyak data
function showMore() {
    document.querySelector('tbody').classList.add('show-more');
    document.getElementById('showMoreBtn').style.display = 'none';
    document.getElementById('showLessBtn').style.display = 'inline-block';
}

// Fungsi untuk menyembunyikan data tambahan
function showLess() {
    document.querySelector('tbody').classList.remove('show-more');
    document.getElementById('showMoreBtn').style.display = 'inline-block';
    document.getElementById('showLessBtn').style.display = 'none';
}

// Tambahkan event listener untuk tombol "Show More" dan "Show Less"
document.getElementById('showMoreBtn').addEventListener('click', showMore);
document.getElementById('showLessBtn').addEventListener('click', showLess);


// form modal
function openModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "block";
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
}

// hapus user
function Hapususer(dataId) {
    var konfirmasi = confirm("Apakah Anda yakin ingin menghapus data?");
    
    if (konfirmasi) {
        // Redirect to the Flask route for deletion
        window.location.href = "/hapus_user/" + dataId;
        return true;
    } else {
        console.log("Penghapusan dibatalkan untuk ID:", dataId);
        return false;
    }
}

// hapus data
function Hapusdata(dataId) {
    var konfirmasi = confirm("Apakah Anda yakin ingin menghapus data?");
    
    if (konfirmasi) {
        // Redirect to the Flask route for deletion
        window.location.href = "/hapus_data/" + dataId;
        return true;
    } else {
        console.log("Penghapusan dibatalkan untuk ID:", dataId);
        return false;
    }
}


// Edit User
function editUser(userId, name, email, password) {
    console.log("Edit User Called:", userId, name, email, password);

    document.getElementById('UserId').value = userId;
    document.getElementById('name').value = name;
    document.getElementById('email').value = email;
    document.getElementById('password').value = password;

    document.getElementById('editForm').action = "/update_user/" + userId;

    document.getElementById('editModal').style.display = 'block';
}


function tutupModal() {
    document.getElementById('editModal').style.display = 'none';
}

function submitForm() {
    console.log("Submit form called");
    document.getElementById('editForm').submit();
}

// Edit Data
function editData(dataId, user, jenis, akurasi) {
    console.log("Edit User Called:", dataId, user, jenis, akurasi);

    document.getElementById('modalDataId').value = dataId;
    document.getElementById('user').value = user;
    document.getElementById('jenis').value = jenis;
    document.getElementById('akurasi').value = akurasi;

    document.getElementById('editForm').action = "/update_data/" + dataId;

    document.getElementById('editModal').style.display = 'block';
}


function tutup() {
    document.getElementById('editModal').style.display = 'none';
}

function submitForm() {
    console.log("Submit form called");
    document.getElementById('editForm').submit();
}