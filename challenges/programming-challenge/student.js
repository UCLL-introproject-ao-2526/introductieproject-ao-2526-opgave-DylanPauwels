function myFirstFunction(bike) {
    forward(bike);
}

function twiceForward(bike) {
    forward(bike);
    forward(bike);
}

function thriceForward(bike) {
    forward(bike);
    forward(bike);
    forward(bike);
}

function forward4(bike) {
    forward(bike);
    forward(bike);
    forward(bike);
    forward(bike);
}

function forward5(bike) {
    let i = 5;

    while (i > 0) {
        forward(bike);
        i = i - 1;
    }
}

function forward10(bike) {
    let i = 10;

    while (i > 0) {
        forward(bike);
        i = i - 1;
    }
}

function right(bike) {
    turnRight(bike);
    forward(bike);
}

function ellShape(bike) {
    forward5(bike);
    turnRight(bike);
    forward4(bike);
}
function uTurn(bike) {
    thriceForward(bike);
    turnRight(bike);
    forward10(bike);
    turnRight(bike);
    twiceForward(bike);
}
function forwardN(bike, steps) {
    let i = steps;

    while (i > 0) {
        forward(bike);
        i = i - 1;
    }
}

function crookedUTurn(bike) {
    forwardN(bike, 7);
    turnRight(bike);
    forwardN(bike, 9);
    turnRight(bike);
    forwardN(bike, 3);
}
function forwardUntilWall(bike) {
    while (!sensor(bike)) {
        forward(bike);
    }
}
function smartEllShape(bike) {
    forwardUntilWall(bike);
    turnRight(bike);
    forwardUntilWall(bike);
}

function spiral(car) {
    while (!sensor(car)) {
        forwardUntilWall(car);
        turnRight(car);
    }
}  
function turnLeft(car) {
    turnRight(car);
    turnRight(car);
    turnRight(car);
}

function left(car) {
    turnLeft(car);
    forward(car);
}

function slalom(car) {
    forwardUntilWall(car);
    turnLeft(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
    turnLeft(car);
    forwardUntilWall(car);
    turnLeft(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
}

function leftOrRight(car) {
    forwardUntilWall(car);
    turnLeft(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
    turnLeft(car);
    forwardUntilWall(car);
}

function incompleteU(car) {
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
    turnRight(car);
    forwardUntilWall(car);
}

function whichDirection(car) {
    while (sensor(car)) {
        turnRight(car);
    }

    forwardUntilWall(car);
}

function sensorRight(car) {
    turnRight(car);
    let result = sensor(car);
    turnLeft(car);

    return result
}

function forwardUntilFreeRight(car) {
    while (sensorRight(car)) {
        forward(car);
    }
}

function firstRight(car) {
    forwardUntilFreeRight(car);
    turnRight(car);
    forwardUntilWall(car);
}

function sensorLeft(car) {
    turnLeft(car);
    let result = sensor(car);
    turnRight(car);

    return result
}

function forwardUntilFreeLeft(car) {
    while (sensorLeft(car)) {
        forward(car);
    }
}

function firstLeft(car) {
    forwardUntilFreeLeft(car);
    turnLeft(car);
    forwardUntilWall(car);
}

function zigZag(car) {
    firstRight(car);
    turnLeft(car);
    forward(car);
    firstLeft(car);
}

function secondRight(car) {
    forwardUntilFreeRight(car);
    forward(car);
    forwardUntilFreeRight(car);
    turnRight(car);
    forwardUntilWall(car);
}

function thirdRight(car) {
    forwardUntilFreeRight(car);
    forward(car);
    forwardUntilFreeRight(car);
    forward(car);
    forwardUntilFreeRight(car);
    turnRight(car);
    forwardUntilWall(car);
}

function forwardUntilNthRight(car, nrights) {
    let i = nrights;

    while (i > 0) {
        forward(car);

        if (!sensorRight(car)) {
            i = i - 1;
        }
    }
}

function fourthRight(car) {
    forwardUntilNthRight(car, 4);
    turnRight(car);
    forwardUntilWall(car);
}

function forwardUntilNthLeft(car, nlefts) {
    let i = nlefts;

    while (i > 0) {
        forward(car);

        if (!sensorLeft(car)) {
            i = i - 1;
        }
    }
}

function fifthLeft(car) {
    forwardUntilNthLeft(car, 5);
    turnLeft(car);
    forwardUntilWall(car);
}

function maze(car) {
    function L(n) {
        forwardUntilNthLeft(car, n);
        turnLeft(car);
    }

    function R(n) {
        forwardUntilNthRight(car, n);
        turnRight(car);
    }

    R(2);
    L(1);
    L(2);
    L(2);
    R(4);
    R(1);
    L(3);
    forwardUntilWall(car);
}

function turnAround(car) {
    turnRight(car);
    turnRight(car);
}

function backward(car) {
    turnAround(car);
    forward(car);
    turnAround(car);
}

function isDeadEnd(car) {
    if (!sensor(car)) {
        return false;
    }

    if (!sensorRight(car)) {
        return false;
    }

    if (!sensorLeft(car)) {
        return false;
    }

    return true
}

function findDeadEnd(car) {
    while (true) {
        forward(car);

        if (isDeadEnd(car)) {
            return;
        }

        backward(car);
        turnRight(car);
    }
}

function follow(car) {
    while (!isGoal()) {
        if (!sensor(car)) {
            forward(car);
        } else if (!sensorRight(car)) {
            turnRight(car);
            forward(car);
        } else {
            turnLeft(car);
            forward(car);
        }
    }

    function isGoal() {
        if (isDeadEnd(car)) {
            return true;
        }

        return false;
    }
}

function rightHand(car) {
    while (!isDeadEnd(car)) {
        if (!sensorRight(car)) {
            turnRight(car);
            forward(car);
        } else if (!sensor(car)) {
            forward(car);
        } else {
            turnLeft(car);
            forward(car);
        }
    }
}

function forwardUntilDestination(car) {
    while (!destinationReached(car)) {
        forward(car);
        
    }
}

function smartForwardUntilWall(car) {
    while (!arrived()) {
        forward(car);
    }

    return destinationReached(car);

    function arrived() {
        if (sensor(car)) {
            return true;
        }

        if (destinationReached(car)) {
            return true;
        }

        return false;
    }
}

function roomba(car) {
    while (true) {
        if (smartForwardUntilWall(car)) {
            return;
        }

        turnRight(car);
        forward(car);
        turnRight(car);

        if (smartForwardUntilWall(car)) {
            return;
        }

        turnLeft(car);
        forward(car);
        turnLeft(car);
    }

}