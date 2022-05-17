const pc_feed = () => {
    const vitals = document.getElementsByClassName('vitals')[0];
    const rover_feed = document.getElementsByClassName('rover-feed')[0];
    const pc_feed = document.getElementsByClassName('pc-feed')[0];
    const history = document.getElementsByClassName('history')[0];
    history.style.display = "none";
    vitals.style.display = "none";
    rover_feed.style.display = "none";
    pc_feed.style.display = "block";
}
const rover_feed = () => {
    const vitals = document.getElementsByClassName('vitals')[0];
    const rover_feed = document.getElementsByClassName('rover-feed')[0];
    const pc_feed = document.getElementsByClassName('pc-feed')[0];
    const history = document.getElementsByClassName('history')[0];
    history.style.display = "none";
    vitals.style.display = "none";
    rover_feed.style.display = "block";
    pc_feed.style.display = "none";
}
const vitals = () => {
    const vitals = document.getElementsByClassName('vitals')[0];
    const rover_feed = document.getElementsByClassName('rover-feed')[0];
    const pc_feed = document.getElementsByClassName('pc-feed')[0];
    const history = document.getElementsByClassName('history')[0];
    history.style.display = "none";
    vitals.style.display = "block";
    rover_feed.style.display = "none";
    pc_feed.style.display = "none";
}
const history = () => {
    const vitals = document.getElementsByClassName('vitals')[0];
    const rover_feed = document.getElementsByClassName('rover-feed')[0];
    const pc_feed = document.getElementsByClassName('pc-feed')[0];
    const history = document.getElementsByClassName('history')[0];
    vitals.style.display = "none";
    rover_feed.style.display = "none";
    pc_feed.style.display = "none";
    history.style.display = "block";
}
const show_all = () => {
    const vitals = document.getElementsByClassName('vitals')[0];
    const rover_feed = document.getElementsByClassName('rover-feed')[0];
    const pc_feed = document.getElementsByClassName('pc-feed')[0];
    const history = document.getElementsByClassName('history')[0];
    history.style.display = "block";
    vitals.style.display = "block";
    rover_feed.style.display = "block";
    pc_feed.style.display = "block";
}
const get_vitals = () => {
    const temp = document.getElementById("temperature");
    const hb = document.getElementById("heartbeat");
    fetch('http://localhost:5000/vitals')
        .then((r) => {
            return r.json()
        })
        .then((data) => {
            temp.innerHTML = data['temperature'] + '°C';
            hb.innerHTML = data['heartbeat'] + ' BPM';
            if (data['message'] !== '') {
                alert(data['message'])
            }
        })
        .catch(() => {
            temp.innerHTML = '--°C';
            hb.innerHTML = '-- BPM';
            console.log('ERROR getting vitals')
        })
}
const get_history = () => {
    const history = document.getElementById("history_table");
    fetch('http://localhost:5000/history')
        .then((r) => {
            return r.json()
        })
        .then((data) => {
            if (document.getElementsByTagName('table').length > 0) {
                history.removeChild(document.getElementsByTagName('table')[0])
            }
            let rows = data['time'].length;
            var tbl = document.createElement('table');
            var tbdy = document.createElement('tbody');
            var th = document.createElement('thead')
            th.appendChild(document.createElement('th')).appendChild(document.createTextNode('Date'));
            th.appendChild(document.createElement('th')).appendChild(document.createTextNode('Time'));
            th.appendChild(document.createElement('th')).appendChild(document.createTextNode('Temperature'));
            th.appendChild(document.createElement('th')).appendChild(document.createTextNode('Heartbeat'));
            th.appendChild(document.createElement('th')).appendChild(document.createTextNode('Message'));
            tbl.appendChild(th)
            for (let i = 0; i < rows; i++) {
                var tr = document.createElement('tr');
                for (let j = 0; j < 5; j++) {
                    var td = document.createElement('td');
                    if (j === 0) {
                        td.appendChild(document.createTextNode('' + data['time'][i].split(' ')[0]));
                    }
                    if (j === 1) {
                        td.appendChild(document.createTextNode('' + data['time'][i].split(' ')[1].split('.')[0]));
                    }
                    if (j === 2) {
                        td.appendChild(document.createTextNode('' + data['temperature'][i]));
                    }
                    if (j === 3) {
                        td.appendChild(document.createTextNode('' + data['heartbeat'][i]));
                    }
                    if (j === 4) {
                        td.appendChild(document.createTextNode('' + data['message'][i]));
                    }
                    tr.appendChild(td)
                }
                tbdy.appendChild(tr)
            }
            tbl.appendChild(tbdy)
            history.appendChild(tbl);
        })
        .catch((reason) => {
            console.log(reason)
        })
}

document.addEventListener("DOMContentLoaded", function (event) {
    setInterval(get_vitals, 2000) // interval value in milliseconds
    setInterval(get_history, 2000) // interval value in milliseconds
})