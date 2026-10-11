const API_BASE_URL = "http://127.0.0.1:8000";

async function apiGet(endpoint) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`);

    if (!response.ok) {
        throw new Error(
            `API error: ${response.status} ${response.statusText}`
        );
    }

    return await response.json();
}

async function getEVs() {
    return await apiGet("/evs/");
}

async function getStations() {
    return await apiGet("/stations/");
}

async function getChargers() {
    return await apiGet("/chargers/");
}

async function createChargingRequest(data) {
    const response = await fetch(
        `${API_BASE_URL}/charging-requests/`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(
            `Request failed (${response.status}): ${errorText}`
        );
    }

    return await response.json();
}