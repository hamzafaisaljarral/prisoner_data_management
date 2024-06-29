document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const prisonerId = urlParams.get('prisoner_id');
    const accessToken = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    if (!prisonerId) {
        window.location.href = './prisoners';
        return;
    }

    if (!accessToken || !refreshToken) {
        window.location.href = '/login';
        return;
    }

    function fetchPrisonerDetails(prisonerId) {
        fetch(`/api/prisoners/${prisonerId}`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        })
        .then(response => {
            if (response.status === 401) {
                // Access token has expired, attempt to refresh it
                return refreshTokenFunc().then(newAccessToken => {
                    if (newAccessToken) {
                        return fetch(`/api/prisoners/${prisonerId}`, {
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
                throw new Error('Failed to fetch prisoner details');
            }
        })
        .then(prisoner => {
            if (prisoner) {
                const detailsContainer = document.getElementById('prisoner-details');
                detailsContainer.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">${prisoner.name}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">ID: ${prisoner.prisoner_id}</h6>
                        <p class="card-text"><strong>Age:</strong> ${prisoner.age}</p>
                        <p class="card-text"><strong>Gender:</strong> ${prisoner.gender}</p>
                        <p class="card-text"><strong>Crime:</strong> ${prisoner.crime.crime_name}</p>
                        <p class="card-text"><strong>Sentence Years:</strong> ${prisoner.sentence_years}</p>
                        <p class="card-text"><strong>Prison:</strong> ${prisoner.prison.prison_name}</p>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load prisoner details.');
        });
    }

    function refreshTokenFunc() {
        return fetch('/api/refresh', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${refreshToken}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                localStorage.setItem('accessToken', data.access_token);
                return data.access_token;
            } else {
                localStorage.removeItem('accessToken');
                localStorage.removeItem('refreshToken');
                window.location.href = '/login';
                return null;
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

    fetchPrisonerDetails(prisonerId);
});
