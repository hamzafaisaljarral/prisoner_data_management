function displayCharts(data) {
    const ctxCrime = document.getElementById('crimeChart').getContext('2d');
    const ctxSentence = document.getElementById('sentenceChart').getContext('2d');
    const ctxGender = document.getElementById('genderChart').getContext('2d');
    const ctxAge = document.getElementById('ageChart').getContext('2d');
    const ctxPrisonPopulation = document.getElementById('prisonPopulationChart').getContext('2d');

    new Chart(ctxCrime, {
        type: 'bar',
        data: {
            labels: Object.keys(data.crime_count),
            datasets: [{
                label: 'Number of Prisoners by Crime Type',
                data: Object.values(data.crime_count),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    new Chart(ctxSentence, {
        type: 'bar',
        data: {
            labels: Object.keys(data.average_sentence_by_crime),
            datasets: [{
                label: 'Average Sentence Length by Crime Type',
                data: Object.values(data.average_sentence_by_crime),
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    new Chart(ctxGender, {
        type: 'pie',
        data: {
            labels: Object.keys(data.gender_distribution),
            datasets: [{
                label: 'Gender Distribution of Prisoners',
                data: Object.values(data.gender_distribution),
                backgroundColor: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)'],
                borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


function displayAgeDistributionChart(data) {
    const ctxAge = document.getElementById('ageChart').getContext('2d');
    new Chart(ctxAge, {
        type: 'bar',
        data: {
            labels: data.map(item => item.age),
            datasets: [{
                label: 'Age Distribution',
                data: data.map(item => item.count),
                backgroundColor: 'rgba(255, 159, 64, 0.2)',
                borderColor: 'rgba(255, 159, 64, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function displayPrisonPopulationChart(data) {
    const ctxPrisonPopulation = document.getElementById('prisonPopulationChart').getContext('2d');
    new Chart(ctxPrisonPopulation, {
        type: 'bar',
        data: {
            labels: data.map(item => item.prison_name),
            datasets: [{
                label: 'Prison Population',
                data: data.map(item => item.count),
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function fetchPrisoners() {
    fetch('/api/prisoners', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            return refreshTokenFunc().then(newAccessToken => {
                if (newAccessToken) {
                    return fetch('/api/prisoners', {
                        headers: {
                            'Authorization': `Bearer ${newAccessToken}`
                        }
                    });
                } else {
                    throw new Error('Failed to refresh token');
                }
            });
        } else if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to fetch prisoners');
        }
    })
    .then(data => {
        if (data) {
            const list = document.getElementById('prisoners-list');
            list.innerHTML = '';  // Clear the list
            data.forEach(prisoner => {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = `/prisoner-details?prisoner_id=${prisoner.prisoner_id}`;
                link.textContent = prisoner.name;
                listItem.appendChild(link);
                list.appendChild(listItem);
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to load prisoners list.');
    });
}

function fetchStatistics() {
    fetch('/api/statistics', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            return refreshTokenFunc().then(newAccessToken => {
                if (newAccessToken) {
                    return fetch('/api/statistics', {
                        headers: {
                            'Authorization': `Bearer ${newAccessToken}`
                        }
                    });
                } else {
                    throw new Error('Failed to refresh token');
                }
            });
        } else if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to fetch statistics');
        }
    })
    .then(data => {
        displayCharts(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to load statistics.');
    });
}

function fetchAgeDistribution() {
    fetch('/api/age-distribution', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            return refreshTokenFunc().then(newAccessToken => {
                if (newAccessToken) {
                    return fetch('/api/age-distribution', {
                        headers: {
                            'Authorization': `Bearer ${newAccessToken}`
                        }
                    });
                } else {
                    throw new Error('Failed to refresh token');
                }
            });
        } else if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to fetch age distribution data');
        }
    })
    .then(data => {
        displayAgeDistributionChart(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to load age distribution data.');
    });
}

function fetchPrisonPopulation() {
    fetch('/api/prison-population', {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('accessToken')}`
        }
    })
    .then(response => {
        if (response.status === 401) {
            return refreshTokenFunc().then(newAccessToken => {
                if (newAccessToken) {
                    return fetch('/api/prison-population', {
                        headers: {
                            'Authorization': `Bearer ${newAccessToken}`
                        }
                    });
                } else {
                    throw new Error('Failed to refresh token');
                }
            });
        } else if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to fetch prison population data');
        }
    })
    .then(data => {
        displayPrisonPopulationChart(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to load prison population data.');
    });
}

function refreshTokenFunc() {
    return fetch('/api/refresh', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('refreshToken')}`
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to refresh token');
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            localStorage.setItem('accessToken', data.access_token);
            return data.access_token;
        } else {
            throw new Error('Failed to obtain new access token');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to refresh token.');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
        return null;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    if (!accessToken || !refreshToken) {
        window.location.href = '/login';
        return;
    }

    fetchPrisoners();
    fetchStatistics();
    fetchAgeDistribution();
    fetchPrisonPopulation();
});
