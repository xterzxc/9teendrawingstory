function $(el) {
    return document.getElementById(el.replace(/#/, ''));
}

var canvas = $('#canvas');
canvas.width = document.body.clientWidth;
canvas.height = document.body.clientHeight;
var context = canvas.getContext('2d');
const undoBtn = document.getElementById('undoBtn');
const redoBtn = document.getElementById('redoBtn');
const clearBtn = document.getElementById('clearBtn');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtn = document.getElementById('closeModalBtn');
const modal = document.getElementById('openModal');

var colorPicker = $('#colorPicker');
var lineWidth = $('#lineWidth');

var undoStack = [];
var redoStack = [];
var isDrawingMode = true;

function fillBackground(color) {
    context.fillStyle = color;
    context.fillRect(0, 0, canvas.width, canvas.height);
}


function getCanvasCoordinates(e) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: (e.clientX || e.targetTouches[0].pageX) - rect.left,
        y: (e.clientY || e.targetTouches[0].pageY) - rect.top
    };
}

function saveState() {
    const currentCanvasState = canvas.toDataURL();
    undoStack.push(currentCanvasState);
    redoStack = [];

    localStorage.setItem('canvasState', currentCanvasState);
    localStorage.setItem('undoStack', JSON.stringify(undoStack));
    localStorage.setItem('redoStack', JSON.stringify(redoStack));
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
        context.lineJoin = "round";
        context.lineWidth = lineWidth.value;

        if (isDrawingMode) {
            context.strokeStyle = colorPicker.value;
        } else {
            context.strokeStyle = '#ffffff';
        }

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

function restoreState(dataURL) {
    if (!dataURL) return;
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
        restoreState(undoStack[undoStack.length - 1]);
    } else if (undoStack.length === 1) {
        redoStack.push(undoStack.pop());
        context.clearRect(0, 0, canvas.width, canvas.height);
        fillBackground('#ffffff');
    }

    localStorage.setItem('canvasState', canvas.toDataURL());
    localStorage.setItem('undoStack', JSON.stringify(undoStack));
    localStorage.setItem('redoStack', JSON.stringify(redoStack));
}

function redo() {
    if (redoStack.length > 0) {
        const lastState = redoStack.pop();
        undoStack.push(lastState);
        restoreState(lastState);
    }

    localStorage.setItem('canvasState', canvas.toDataURL());
    localStorage.setItem('undoStack', JSON.stringify(undoStack));
    localStorage.setItem('redoStack', JSON.stringify(redoStack));
}

undoBtn.addEventListener('click', undo);
redoBtn.addEventListener('click', redo);

const modeSwitch = $('#modeSwitch');
modeSwitch.addEventListener('change', function() {
    isDrawingMode = !modeSwitch.checked;
});

lineWidth.addEventListener('input', function() {
    context.lineWidth = lineWidth.value;
});

function clear() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    fillBackground('#ffffff');
    undoStack.splice(0, undoStack.length);
    redoStack.splice(0, redoStack.length);

    localStorage.removeItem('canvasState');
}
clearBtn.addEventListener('click', clear);

openModalBtn.addEventListener('click', function() {
    modal.classList.add('show');
});

closeModalBtn.addEventListener('click', function() {
    modal.classList.remove('show');
});

window.addEventListener('click', function(event) {
    if (event.target == modal) {
        modal.classList.remove('show');
    }
});

document.addEventListener('keydown', function(e) {

    const isModalOpen = modal.classList.contains('show');

    if (!isModalOpen) {
        if ((e.ctrlKey && e.key === 'z') || e.code === 'KeyZ') {
            e.preventDefault();
            undo();
        } else if ((e.ctrlKey && e.key === 'y') || e.code === 'KeyY') {
            e.preventDefault();
            redo();
        }
    }
});








document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        var loader = document.getElementById('loader');
        var content = document.getElementById('content');

        loader.classList.add('hidden');

        content.classList.remove('hidden');
        content.classList.add('visible');


        setTimeout(function() {
            loader.remove();
        }, 500);
    }, 500);


    const savedImageData = localStorage.getItem('canvasState');
    if (savedImageData) {
        const img = new Image();
        img.src = savedImageData;
        img.onload = function() {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(img, 0, 0);
        };
    } else {
        fillBackground('#ffffff');
    }

    const savedUndoStack = localStorage.getItem('undoStack');
    const savedRedoStack = localStorage.getItem('redoStack');

    if (savedUndoStack) {
        undoStack = JSON.parse(savedUndoStack);
    } else {
        undoStack = [];
    }

    if (savedRedoStack) {
        redoStack = JSON.parse(savedRedoStack);
    } else {
        redoStack = [];
    }
});