function degToRad(degree) {
    let factor = Math.PI / 180;
    return degree * factor;
    let canvas = document.getElementById("canvas");
    canvas.width = innerWidth;
    canvas.height = innerHeight;

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


    let countDown = new Date(last_fed).getTime(),
        x = setInterval(function () {
            let now = new Date().getTime(),
                distance = now - countDown;
                if (distance < 0) {
                    distance = 0;
                }
            
            (document.getElementById("days").innerText = Math.floor(distance / day)),
                (document.getElementById("hours").innerText = Math.floor(
                    (distance % day) / hour
                )),
                (document.getElementById("minutes").innerText = Math.floor(
                    (distance % hour) / minute
                )),
                (document.getElementById("seconds").innerText = Math.floor(
                    (distance % minute) / second
                ));


            let ctx1 = canvas.getContext("2d");
            //Arch porperties
            ctx1.strokeStyle = 'darkgreen';
            ctx1.shadowColor = 'darkgreen';
            ctx1.lineWidth = 25;
            ctx1.shadowBlur = 1;

            //Hours
            //calcualte set intervale between jumps always 2 days ahead 
            //update every minute
            ctx1.beginPath();
            //      pos,pos,size
            ctx1.arc(250, 250, 200, degToRad(270),degToRad(270+(360*(1-((distance)/(2*day))))));
            ctx1.stroke();

            //do something later when date is reached
            if (distance == 0) {
                //let countDown = new Date(start).getTime()

                headline.innerText = "Composter needs fed!";
                //countdown.style.display = "none";
                //Clear the arc after countdown ends
                //ctx1.clearRect(0, 0, canvas.width, canvas.height);
                
                // ctx1.beginPath()
                ctx1.strokeStyle = 'red';
                ctx1.shadowColor = 'red';
                //ctx1.font = "30px Helvetica";
                //ctx1.fillStyle = 'rgb(234,197,16)';
                //ctx1.fillText("Composter Needs Fed!", 100, 250);
                clearInterval(x);
            }
            //seconds
        }, 0);
    };
})();
