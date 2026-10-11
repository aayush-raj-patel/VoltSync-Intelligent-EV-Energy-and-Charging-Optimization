function renderTable(headId, bodyId, data) {
    const head = document.getElementById(headId);
    const body = document.getElementById(bodyId);

    head.replaceChildren();
    body.replaceChildren();

    if (!Array.isArray(data) || data.length === 0) {
        body.innerHTML =
            '<tr><td>No records found</td></tr>';
        return;
    }

    const columns = Object.keys(data[0]);

    const headerRow = document.createElement("tr");

    columns.forEach(column => {
        const th = document.createElement("th");
        th.textContent = column;
        headerRow.appendChild(th);
    });

    head.appendChild(headerRow);

    data.forEach(item => {
        const row = document.createElement("tr");

        columns.forEach(column => {
            const td = document.createElement("td");
            const value = item[column];

            td.textContent =
                value === null || value === undefined
                    ? "—"
                    : typeof value === "object"
                        ? JSON.stringify(value)
                        : String(value);

            row.appendChild(td);
        });

        body.appendChild(row);
    });
}

async function loadDashboard() {
    const message = document.getElementById("message");
    message.textContent = "Loading data...";

    try {
        const [evs, stations, chargers] = await Promise.all([
            getEVs(),
            getStations(),
            getChargers()
        ]);

        document.getElementById("ev-count").textContent =
            evs.length;

        document.getElementById("station-count").textContent =
            stations.length;

        document.getElementById("charger-count").textContent =
            chargers.length;

        renderTable("ev-head", "ev-body", evs);
        renderTable("station-head", "station-body", stations);
        renderTable("charger-head", "charger-body", chargers);

        message.textContent = "Dashboard data loaded successfully.";
        message.className = "alert alert-success mb-3";
    } catch (error) {
        message.textContent =
            "Could not load dashboard data.\n" + error.message;

        message.className = "alert alert-danger mb-3";
    }
}

document.addEventListener("DOMContentLoaded", loadDashboard);

function fillSelect(selectId, items, idKey, labelKey) {
    const select = document.getElementById(selectId);

    select.replaceChildren(new Option("Select an option", ""));

    items.forEach(item => {
        const label = item[labelKey] ?? `ID ${item[idKey]}`;

        select.add(new Option(label, item[idKey]));
    });
}

async function loadRequestOptions() {
    try {
        const [evs, stations] = await Promise.all([
            getEVs(),
            getStations()
        ]);

        fillSelect("ev-id", evs, "ev_id", "model");
        fillSelect("station-id", stations, "station_id", "name");
    } catch (error) {
        document.getElementById("request-message").textContent =
            "Could not load EV/station options: " + error.message;
    }
}

document.getElementById("charging-request-form")
    .addEventListener("submit", async function (event) {
        event.preventDefault();

        const message = document.getElementById("request-message");

        const data = {
            ev_id: Number(document.getElementById("ev-id").value),
            station_id: Number(document.getElementById("station-id").value),
            required_energy: Number(
                document.getElementById("required-energy").value
            ),
            expected_departure_time:
                document.getElementById("departure-time").value
        };

        try {
            const result = await createChargingRequest(data);

            message.textContent =
                "Charging request created! " + JSON.stringify(result);

            message.className = "alert alert-success mt-3";
        } catch (error) {
            message.textContent =
                "Request failed: " + error.message;

            message.className = "alert alert-danger mt-3";
        }
    });

loadRequestOptions();