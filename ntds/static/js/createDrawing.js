document.addEventListener('DOMContentLoaded', function() {
    initializeCanvas();

    setTimeout(function() {
        const loader = document.getElementById('loader');
        const content = document.getElementById('content');

        if (loader && content) {
            loader.classList.add('hidden');
            content.classList.remove('hidden');
            content.classList.add('visible');

            setTimeout(function() {
                if (loader) loader.remove();
            }, 500);
        }
    }, 500);
});

function $(el) {
    return document.getElementById(el.replace(/#/, ''));
}

function initializeCanvas() {
    const canvas = $('#canvas');
    if (!canvas) return;

    canvas.width = document.body.clientWidth;
    canvas.height = document.body.clientHeight;
    const context = canvas.getContext('2d');
    const colorPicker = $('#colorPicker');
    const lineWidth = $('#lineWidth');
    const undoBtn = $('#undoBtn');
    const redoBtn = $('#redoBtn');
    const clearBtn = $('#clearBtn');
    const openModalBtn = $('#openModalBtn');
    const closeModalBtn = $('#closeModalBtn');
    const modal = $('#openModal');
    const modeSwitch = $('#modeSwitch');

    let undoStack = [];
    let redoStack = [];
    let isDrawingMode = true;

    function fillBackground(color) {
        context.fillStyle = color;
        context.fillRect(0, 0, canvas.width, canvas.height);
    }

    function getCanvasCoordinates(e) {
        const rect = canvas.getBoundingClientRect();
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

    function restoreState(dataURL) {
        if (!dataURL) return;
        const img = new Image();
        img.src = dataURL;
        img.onload = () => {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(img, 0, 0);
        };
    }

    function start(coors) {
        if (!this.isDrawing) {
            context.beginPath();
            context.moveTo(coors.x, coors.y);
            this.isDrawing = true;
        }
    }

    function move(coors) {
        if (this.isDrawing) {
            context.lineJoin = "round";
            context.lineWidth = lineWidth.value;

            context.strokeStyle = isDrawingMode ? colorPicker.value : '#ffffff';

            context.lineTo(coors.x, coors.y);
            context.stroke();
        }
    }

    function stop(coors) {
        if (this.isDrawing) {
            move(coors);
            this.isDrawing = false;
            saveState();
        }
    }

    const drawer = {
        isDrawing: false,
        mousedown: start,
        mousemove: move,
        mouseup: stop,
        touchstart: start,
        touchmove: move,
        touchend: stop
    };

    function draw(e) {
        const coors = getCanvasCoordinates(e);
        drawer[e.type](coors);
    }

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
            restoreState(undoStack[undoStack.length - 1]);
        }
    };

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

    modeSwitch.addEventListener('change', function() {
        isDrawingMode = !modeSwitch.checked;
    });

    lineWidth.addEventListener('input', function() {
        context.lineWidth = lineWidth.value;
    });

    function clear() {
        context.clearRect(0, 0, canvas.width, canvas.height);
        fillBackground('#ffffff');
        undoStack = [];
        redoStack = [];

        localStorage.removeItem('canvasState');
        localStorage.removeItem('undoStack');
        localStorage.removeItem('redoStack');
    }

    clearBtn.addEventListener('click', clear);

    openModalBtn.addEventListener('click', function() {
        modal.classList.add('show');
    });

    closeModalBtn.addEventListener('click', function() {
        modal.classList.remove('show');
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
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
            } else if (e.key === 'g' || e.code === 'KeyG') {
                e.preventDefault();
                modeSwitch.checked = !modeSwitch.checked;
                isDrawingMode = !modeSwitch.checked;
            } else if (e.key === 'c' || e.code === 'KeyC') {
                e.preventDefault();
                clear();
            } else if (e.key === 's' || e.code === 'KeyS') {
                e.preventDefault();
                colorPicker.click();
            }
        }
    });


    document.addEventListener('wheel', function(e) {
        const isModalOpen = modal.classList.contains('show');
    
        if (!isModalOpen) {
            let currentLineWidth = parseInt(lineWidth.value);
            if (e.deltaY > 0) {
                lineWidth.value = Math.max(1, currentLineWidth - 1);
                context.lineWidth = lineWidth.value;
            } else if (e.deltaY < 0) {
                lineWidth.value = Math.min(100, currentLineWidth + 1);
                context.lineWidth = lineWidth.value;
            }
        }
    });

    const savedImageData = localStorage.getItem('canvasState');
    if (savedImageData) {
        restoreState(savedImageData);
    } else {
        fillBackground('#ffffff');
    }

    const savedUndoStack = localStorage.getItem('undoStack');
    if (savedUndoStack) {
        undoStack = JSON.parse(savedUndoStack);
    }

    const savedRedoStack = localStorage.getItem('redoStack');
    if (savedRedoStack) {
        redoStack = JSON.parse(savedRedoStack);
    }
}

function downloadCanvasImage() {
    const canvas = document.getElementById('canvas');
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = 'drawing.png';
    link.click(); 
}

document.getElementById('download').addEventListener('click', downloadCanvasImage);