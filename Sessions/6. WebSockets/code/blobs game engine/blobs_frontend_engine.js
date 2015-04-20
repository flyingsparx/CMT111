function Game(){
    this.started = false;
    var elem = null;
    var players = [];
    var food = null;

    var update_game = function(){
        for(var i = 0; i < players.length; i++){
            var p = players[i];
            var p_elem = document.getElementById("player_"+p.name);
            p_elem.style.backgroundColor=p.colour;
            p_elem.style.borderRadius="50%";
            p_elem.style.width="20px";
            p_elem.style.height="20px";
            p_elem.style.position="absolute";
            p_elem.style.top=p.y*20+"px";
            p_elem.style.left=p.x*20+"px";
            p_elem.style.color="white";
            p_elem.style.textAlign="center";
            p_elem.style.fontWeight="bold";
            p_elem.innerHTML = p.score;
        } 
        var f_elem = document.getElementById("food");
        f_elem.style.backgroundColor="white";
        f_elem.style.borderRadius="50%";
        f_elem.style.height="20px";
        f_elem.style.width="20px";
        f_elem.style.position="absolute";
        f_elem.style.top=food.y*20+"px";
        f_elem.style.left=food.x*20+"px";
    };

    this.init = function(id){
        if(id == null || id == undefined){
            document.getElementsByTagName("body")[0].innerHTML += '<div id="game"></div>';
            id = "game";
        }
        elem = document.getElementById(id);

        elem.style.position="relative";
        elem.style.display="block";
        elem.style.margin="10px auto";
        elem.style.backgroundColor="green";
        elem.style.width="400px";
        elem.style.height="400px";
        elem.style.border="1px solid gray";
        for(var i = 0; i < 20; i++){
            for(var j = 0; j < 20; j++){
                var square='<div style="top:'+i*20+'px;left:'+j*20+'px;" class="square"></div>';
                elem.innerHTML+=square;
            }
        }
        var squares = elem.getElementsByClassName("square");
        for(var i = 0; i < squares.length; i++){
            var square = squares[i];
            square.style.position="absolute";
            square.style.width="18px";
            square.style.height="18px";
            square.style.border="1px solid white";
        }
        elem.innerHTML+='<div id="food"></div>';
        this.started = true;
        food = {};
        food.x=0;food.y=0;
    };
    
    this.update_player = function(player){
        for(var i = 0; i < players.length; i++){
            if(players[i].name==player.name){
                players[i].x=player.x;
                players[i].y=player.y;
                players[i].score=player.score;
                update_game();
                return;
            }
        }
        elem.innerHTML+='<div class="player" id="player_'+player.name+'"></div>';
        players.push(player);
        update_game();
    };

    this.update_food = function(f){
        food = f;
        update_game(); 
    }
}
