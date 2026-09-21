/* ==========================================================================
   EduLead School Dashboard - Chart.js & Admin Interactions
   ========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Mobile Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Student Overview Line Chart (This Academic Year)
    const studentLineCtx = document.getElementById('studentLineChart');
    if (studentLineCtx) {
        new Chart(studentLineCtx.getContext('2d'), {
            type: 'line',
            data: {
                labels: ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Mar'],
                datasets: [{
                    label: 'Enrolled Students',
                    data: [300, 480, 520, 680, 650, 890, 920, 1200],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#2563eb',
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // Attendance Overview Donut Chart (This Month)
    const attendanceChartCtx = document.getElementById('attendanceChart');
    if (attendanceChartCtx) {
        new Chart(attendanceChartCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Present', 'Absent', 'Leave'],
                datasets: [{
                    data: [85, 10, 5],
                    backgroundColor: ['#10b981', '#ef4444', '#f59e0b'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '72%',
                plugins: {
                    legend: { position: 'right' }
                }
            }
        });
    }
});
