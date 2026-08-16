// FUZZYHASH ANALYZER - DASHBOARD CHARTS JS (Chart.js)

document.addEventListener('DOMContentLoaded', () => {
    const distCanvas = document.getElementById('similarityDistChart');
    const timelineCanvas = document.getElementById('activityTimelineChart');

    if (!distCanvas && !timelineCanvas) return;

    fetch('/api/dashboard_metrics')
        .then(res => res.json())
        .then(data => {
            if (distCanvas && data.distribution) {
                new Chart(distCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: data.distribution.labels,
                        datasets: [{
                            data: data.distribution.data,
                            backgroundColor: ['#f43f5e', '#f59e0b', '#10b981'],
                            borderColor: '#1e293b',
                            borderWidth: 2
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { color: '#94a3b8', font: { size: 11 } }
                            }
                        }
                    }
                });
            }

            if (timelineCanvas && data.timeline) {
                new Chart(timelineCanvas, {
                    type: 'line',
                    data: {
                        labels: data.timeline.labels.length ? data.timeline.labels : ['Today'],
                        datasets: [{
                            label: 'Analyses Run',
                            data: data.timeline.data.length ? data.timeline.data : [1],
                            borderColor: '#06b6d4',
                            backgroundColor: 'rgba(6, 182, 212, 0.15)',
                            fill: true,
                            tension: 0.3
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } },
                            y: { ticks: { color: '#94a3b8', stepSize: 1 }, grid: { color: '#334155' } }
                        },
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            }
        })
        .catch(err => console.log('Metrics chart load note:', err));
});
