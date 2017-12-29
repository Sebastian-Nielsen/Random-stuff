
console.log('succesfully injected external js file');            
function openWIndow(url, idpage) {
                    alert('It worked!');
                    var idbutton = $(".button");
                    idbutton.attr("disabled", "disabled").css("opacity", ".6");

                    var seconds = 20;
                    if(flag == 4){
                        seconds = 30;
                    }   
                    var pivot = 0;
                    var id = $("#" + idpage);
                    var conteinerttitle = id.find('.containertitle');

                    var j = 0;


                    token = conteinerttitle.attr('data-token');


                    if(flag != 6){
                     $.get("https://kingdomlikes.com/free_points/count", {token: conteinerttitle.attr('id'), type: flag, csf: $("#token").attr("value")}, function (data) {
                            if(data["success"]){
                                token = data["count"];
                            }else{
                                token = conteinerttitle.attr('data-token');
                            }
                            });
                    }


                                      var windowchild = window.open(url, "", "width=1100, height=650,scrollbars=1");
                                             
                                        
                    var deamon = setInterval(function ()
                    {
                                            if (windowchild.closed || j > seconds) {
                                        
                    idbutton.removeAttr("disabled").css("opacity", "1");

                            var idmask = id.find(".mask");
                            idmask.fadeIn(0);
                            var target = document.getElementById(idpage);
                            var spinner = new Spinner(opts).spin(target);
                            var idmessage = id.find(".message");
                            idmessage.fadeIn();
                            windowchild.close();
                            clearInterval(deamon);
                            
                            $.post("https://kingdomlikes.com/free_points/check", {token: token, id: conteinerttitle.attr('id'), check:pivot, csf: $("#token").attr("value"), aaizwjmpavngm: fuckyou}, function (data) {
                            spinner.stop();
                             if (data['success']){
                                 message = '<h3>¡Congratulations! You earn <span class = "bluefont" >' + data['CPC']+ ' points. </span>There was added to your balance. </h3><img class="sprite sprite-true120" alt="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHUAAAB1AQMAAABKyjz/AAAAA1BMVEX///+nxBvIAAAAAXRSTlMAQObYZgAAABdJREFUeNpjYBgFo2AUjIJRMApGAaUAAAdQAAGTFslZAAAAAElFTkSuQmCC">';
                             }else{
                                 message = error;
                             }
                                    idmessage.html(message).delay(timedelay).fadeOut("fast", function () {
                            if (data['success']) {
                            $('#points').html(formatNumber(parseInt(data['points'])));
                                    //changePage(idpage,flag);
                                    getPages(idpage.slice(-1), false);
                            } else {
                            $(this).empty();
                                    idmask.fadeOut("fast");
                            }
                            });
                            });
                    }
                                        
                            j++;
                    }, 500);
            }
            getPages(5, true);

function testing() {
            console.log('YES THIS ALSO WORKED');
            alert('123');
}
