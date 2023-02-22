function degToRad(degree) {
    let factor = Math.PI / 180;
    return degree * factor;
}

(function () {
    const second = 1000,
        minute = second * 60,
        hour = minute * 60,
        day = hour * 24;

    window.onload = init;

    function init() {
        var last_fed_string = document.getElementById("composter_last_fed").getAttribute('jsvalue');
        const last_fed = new Date(last_fed_string);

        let countDown = new Date(last_fed).getTime() + 2 * day,
            x = setInterval(function () {
                let now = new Date().getTime(),
                    distance = countDown - now;
                if (distance < 0) {
                    distance = 0;
                }

                const percentage = 1 - distance / (2 * day);

                (document.getElementById("days").innerText = Math.floor(distance / day)),
                    (document.getElementById("hours").innerText = Math.floor((distance % day) / hour)),
                    (document.getElementById("minutes").innerText = Math.floor((distance % hour) / minute)),
                    (document.getElementById("seconds").innerText = Math.floor((distance % minute) / second));

                let ctx1 = canvas.getContext("2d");

                // Arch properties
                ctx1.lineWidth = 35;
                ctx1.shadowColor = 'white';
                ctx1.shadowBlur = 2;


                // Fill with blue
                ctx1.beginPath();
                ctx1.strokeStyle = "red";
                ctx1.arc(250, 250, 200, 0, 2 * Math.PI);
                ctx1.stroke();

                // Fill with green
                ctx1.beginPath();
                ctx1.strokeStyle = "green";
                ctx1.arc(250, 250, 200, degToRad(270), degToRad(270 + 360 * percentage));
                ctx1.stroke();

                // do something later when date is reached
                if (distance == 0) {
                    headline.innerText = "Composter needs fed!";
                    clearInterval(x);
                }
            }, 0);


    };
})();
