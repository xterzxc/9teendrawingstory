function $(el) {
    return document.getElementById(el.replace(/#/, ''));
}


var canvas = $('#canvas');
canvas.width = document.body.clientWidth;
canvas.height = document.body.clientHeight;
var context = canvas.getContext('2d');
const undoBtn = document.getElementById('undoBtn');
const redoBtn = document.getElementById('redoBtn');
const saveBtn = document.getElementById('saveBtn');
const clearBtn = document.getElementById('clearBtn');



var colorPicker = $('#colorPicker');
var lineWidth = $('#lineWidth');

var undoStack = [];
var redoStack = [];

function fillBackground(color) {
    context.fillStyle = color;
    context.fillRect(0, 0, canvas.width, canvas.height);
}

// Заполняем холст фоном при загрузке
fillBackground('#ffffff'); // Белый фон

function getCanvasCoordinates(e) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: (e.clientX || e.targetTouches[0].pageX) - rect.left,
        y: (e.clientY || e.targetTouches[0].pageY) - rect.top
    };
}

function saveState() {
    undoStack.push(canvas.toDataURL());
    redoStack = [];
}

var start = function(coors) {
    if (!this.isDrawing) {
        context.beginPath();
        context.moveTo(coors.x, coors.y);
        this.isDrawing = true;
    }
};

var move = function(coors) {
    if (this.isDrawing) {
        context.strokeStyle = colorPicker.value;
        context.lineJoin = "round";
        context.lineWidth = lineWidth.value;
        context.lineTo(coors.x, coors.y);
        context.stroke();
    }
};

var stop = function(coors) {
    if (this.isDrawing) {
        move(coors);
        this.isDrawing = false;
        saveState();
    }
};

var drawer = {
    isDrawing: false,
    mousedown: start,
    mousemove: move,
    mouseup: stop,
    touchstart: start,
    touchmove: move,
    touchend: stop
};

var draw = function(e) {
    var coors = getCanvasCoordinates(e);
    drawer[e.type](coors);
};

canvas.addEventListener('mousedown', draw, false);
canvas.addEventListener('mousemove', draw, false);
canvas.addEventListener('mouseup', draw, false);
canvas.addEventListener('touchstart', draw, false);
canvas.addEventListener('touchmove', draw, false);
canvas.addEventListener('touchend', draw, false);

document.body.addEventListener('touchmove', function(e) {
    e.preventDefault();
}, false);

window.onresize = function(e) {
    canvas.width = document.body.clientWidth;
    canvas.height = document.body.clientHeight;
    if (undoStack.length > 0) {
        restoreState(undoStack, false);
    }
};

function restoreState(stack, pop = true) {
    if (stack.length === 0) return;
    const dataURL = stack[stack.length - 1];
    if (pop) stack.pop()
    const img = new Image();
    img.src = dataURL;
    img.onload = () => {
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(img, 0, 0);
    };
}

function undo() {
    if (undoStack.length > 1) {
        redoStack.push(undoStack.pop());
        restoreState(undoStack, false);
    } else if (undoStack.length === 1) {
        redoStack.push(undoStack.pop());
        context.clearRect(0, 0, canvas.width, canvas.height);
    }
}

function redo() {
    if (redoStack.length > 0) {
        const lastState = redoStack.pop();
        undoStack.push(lastState);
        restoreState(undoStack, false);
    }
}

undoBtn.addEventListener('click', undo);
redoBtn.addEventListener('click', redo);

saveBtn.addEventListener('click', function() {
    const dataURL = canvas.toDataURL('image/png');
    
    const link = document.createElement('a');
    link.href = dataURL;
    link.download = 'canvas-image.png'; 
    link.click();
});

document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'z' || e.code === 'KeyZ') {
        e.preventDefault(); 
        undo();
    } else if (e.ctrlKey && e.key === 'y' || e.code === 'KeyY') {
        e.preventDefault(); 
        redo();
    }
});

function clear(){
    context.clearRect(0, 0, canvas.width, canvas.height);
    undoStack.splice(0, undoStack.length);
    redoStack.splice(0, redoStack.length);
};  
clearBtn.addEventListener('click', clear);