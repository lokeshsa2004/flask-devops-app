/* ==========================================
   DASHBOARD JAVASCRIPT - User Management
   ========================================== */

let currentEditingUserId = null;

/**
 * Show add user modal
 */
function showAddUserModal() {
    currentEditingUserId = null;
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    document.getElementById('modalTitle').textContent = 'Add New User';
    document.getElementById('userModal').classList.add('show');
}

/**
 * Close user modal
 */
function closeUserModal() {
    document.getElementById('userModal').classList.remove('show');
    currentEditingUserId = null;
}

/**
 * Load user data for editing
 */
async function editUser(userId) {
    try {
        const user = await apiRequest(`/api/users/${userId}`);
        currentEditingUserId = userId;

        document.getElementById('userId').value = user.id;
        document.getElementById('username').value = user.username;
        document.getElementById('email').value = user.email;
        document.getElementById('firstName').value = user.first_name || '';
        document.getElementById('lastName').value = user.last_name || '';
        document.getElementById('bio').value = user.bio || '';
        document.getElementById('isActive').checked = user.is_active;

        document.getElementById('modalTitle').textContent = `Edit User: ${user.username}`;
        document.getElementById('userModal').classList.add('show');
    } catch (error) {
        showNotification('Failed to load user data', 'error');
    }
}

/**
 * Handle user form submission
 */
async function handleUserSubmit(event) {
    event.preventDefault();

    const userId = document.getElementById('userId').value;
    const formData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        first_name: document.getElementById('firstName').value,
        last_name: document.getElementById('lastName').value,
        bio: document.getElementById('bio').value,
        is_active: document.getElementById('isActive').checked,
    };

    try {
        if (userId) {
            // Update existing user
            await apiRequest(`/api/users/${userId}`, {
                method: 'PUT',
                body: JSON.stringify(formData),
            });
            showNotification('User updated successfully!', 'success');
        } else {
            // Create new user
            await apiRequest('/api/users', {
                method: 'POST',
                body: JSON.stringify(formData),
            });
            showNotification('User created successfully!', 'success');
        }

        closeUserModal();
        // Reload the table
        await loadUsersTable();
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    }
}

/**
 * Delete user
 */
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) {
        return;
    }

    try {
        await apiRequest(`/api/users/${userId}`, {
            method: 'DELETE',
        });
        showNotification('User deleted successfully!', 'success');
        await loadUsersTable();
    } catch (error) {
        showNotification(`Error: ${error.message}`, 'error');
    }
}

/**
 * Load users table via API
 */
async function loadUsersTable() {
    const page = new URLSearchParams(window.location.search).get('page') || 1;

    try {
        const data = await apiRequest(`/api/users?page=${page}&per_page=10`);
        const tbody = document.getElementById('users-tbody');

        if (data.users.length === 0) {
            tbody.innerHTML =
                '<tr><td colspan="8" class="text-center">No users found. <a href="#" onclick="showAddUserModal(); return false;">Add the first user</a></td></tr>';
            return;
        }

        tbody.innerHTML = data.users
            .map(
                (user) => `
            <tr class="user-row" data-user-id="${user.id}">
                <td>${user.id}</td>
                <td><strong>${user.username}</strong></td>
                <td>${user.email}</td>
                <td>${(user.first_name || '') + ' ' + (user.last_name || '')}</td>
                <td>${
                    user.bio && user.bio.length > 30
                        ? user.bio.substring(0, 30) + '...'
                        : user.bio || '-'
                }</td>
                <td>
                    <span class="status-badge ${user.is_active ? 'active' : 'inactive'}">
                        ${user.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>${formatDate(user.created_at)}</td>
                <td class="actions">
                    <button class="btn btn-sm btn-edit" onclick="editUser(${user.id})">Edit</button>
                    <button class="btn btn-sm btn-delete" onclick="deleteUser(${user.id})">Delete</button>
                </td>
            </tr>
        `
            )
            .join('');
    } catch (error) {
        showNotification('Failed to load users', 'error');
    }
}

/**
 * Filter users by search
 */
function filterUsers() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const rows = document.querySelectorAll('.user-row');

    rows.forEach((row) => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchInput) ? '' : 'none';
    });
}

/**
 * Close modal when clicking outside
 */
document.addEventListener('click', function (event) {
    const modal = document.getElementById('userModal');
    if (modal && event.target === modal) {
        closeUserModal();
    }
});

/**
 * Close modal with Escape key
 */
document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        closeUserModal();
    }
});

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', function () {
    // The table is already populated by the server
    // This is here for potential future enhancements
    console.log('Dashboard initialized');
});
