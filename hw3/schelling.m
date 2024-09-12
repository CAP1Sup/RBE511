function [] = schelling()
    clc;
    clear;
    close all;

    thresholds = [3, 4]; % update as necessary
    popPers = [0.6, 0.8]; % update as necessary
    simluations = size(thresholds, 2) ^ size(popPers, 2);

    parfor sim = 1:simluations
        popPer = popPers(ceil(sim / size(thresholds, 2)));
        threshold = thresholds(mod(sim - 1, size(thresholds, 2)) + 1);

        % Initialize grid
        grid = initGrid(popPer);

        % Save and display First Grid
        figure
        displayGrid(grid, sprintf('Pop %0.2f, Threshold %d, Initial Frame', popPer, threshold))
        saveas(gcf, sprintf('Pop%0.2f_Threshold%d_Initial.png', popPer, threshold));

        mainModel(grid, popPer, threshold);
    end

end

function grid = initGrid(populationPercentage)
    % we want, X(1) and O(-1) to take 20% each of the grid
    % and blank space(0) remaining 60%
    % reducing these numbers we can say that out of 5 entries we want
    % three empty space(0), one X(1) and one O(-1)
    if populationPercentage == 0.6
        ratio = [0 0 0 -1 1]; % Proportion of the grid divided as per members
    elseif populationPercentage == 0.8
        ratio = [0 -1 -1 1 1]; % Proportion of the grid divided as per members
    end

    temp = repmat(ratio, 1, 500); % randomly repeat this for 500 times
    temp = temp(randperm(numel(temp))); % Jumble up those entries
    grid = reshape(temp, [50, 50]);
end

function [] = displayGrid(currGrid, titleString)
    imagesc(currGrid)
    cmap = flag(3);
    colormap(cmap);
    hold on
    entry = line(ones(3), ones(3));
    set(entry, {'color'}, mat2cell(cmap, ones(1, 3), 3));
    legend('X', 'empty', 'O')
    title(titleString)
    xlabel('Y')
    ylabel('X')
    hold off
end

function [] = mainModel(grid, popPer, threshold)
    %gridSatisfactionFlag = false;
    iterations = 1;
    maxIterations = 1000;
    imgSaveItr = 100;
    %     while (gridSatisfactionFlag == false)
    while (iterations <= maxIterations)
        disp(sprintf('Population Percentage %0.2f, Threshold %d, Iteration %d', popPer, threshold, iterations))
        grid = mainShifting(grid, threshold);

        if iterations == 1 || (mod(iterations, imgSaveItr) == 0) || iterations == maxIterations
            h = figure;
            displayGrid(grid, sprintf('Population Percentage %0.2f, Threshold %d, Iteration %d', popPer, threshold, iterations))
            saveas(h, sprintf('Pop%0.2f_Threshold%d_Iteration%d.png', popPer, threshold, iterations));
        end

        iterations = iterations + 1;
    end

end

function grid = mainShifting(grid, threshold)
    x = 1;
    y = 2;
    unhappyLocations = getAllUnhappy(grid, threshold);

    for unhappyIndex = 1:length(unhappyLocations)
        currSadAgentLoc = unhappyLocations(unhappyIndex, :);
        currSadAgentVal = grid(currSadAgentLoc(x), currSadAgentLoc(y));
        closestValidPoint = getClosestNewValidPoint(currSadAgentVal, currSadAgentLoc, grid, threshold);
        grid = swapPoints(currSadAgentLoc, closestValidPoint, grid);
    end

end

function unHappy = getAllUnhappy(currGrid, threshold)
    unHappy = [];
    gridSize = size(currGrid);

    for x = 1:gridSize(1)

        for y = 1:gridSize(2)
            currentCellValue = currGrid(x, y);
            location = [x, y];

            if not(isValid(currentCellValue, location, currGrid, threshold))
                unHappy = [unHappy; x, y];
            end

        end

    end

end

% Returns a list of empty points in the grid
function emptyCells = getAllEmptyCells(currGrid)
    emptyCells = [];
    EMPTY = 0;
    gridSize = size(currGrid);

    for x = 1:gridSize(1)

        for y = 1:gridSize(2)
            currentCellValue = currGrid(x, y);

            if currentCellValue == EMPTY
                emptyCells = [emptyCells; x, y];
            end

        end

    end

end

% Returns a list of neighbors of 8 indices for a given location
function neighborLocations = getNeighborLocations(loc, currGrid)
    neighborLocations = [];
    x = loc(1);
    y = loc(2);
    gridSize = size(currGrid);

    % Right side
    if x < gridSize(1)
        neighborLocations = [neighborLocations; x + 1, y];

        % Top right
        if y > 1
            neighborLocations = [neighborLocations; x + 1, y - 1];
        end

        % Bottom right
        if y < gridSize(2)
            neighborLocations = [neighborLocations; x + 1, y + 1];
        end

    end

    % Bottom side
    if y < gridSize(2)
        neighborLocations = [neighborLocations; x, y + 1];
    end

    % Left side
    if x > 1
        neighborLocations = [neighborLocations; x - 1, y];

        % Top left
        if y > 1
            neighborLocations = [neighborLocations; x - 1, y - 1];
        end

        % Bottom left
        if y < gridSize(2)
            neighborLocations = [neighborLocations; x - 1, y + 1];
        end

    end

    % Top side
    if y > 1
        neighborLocations = [neighborLocations; x, y - 1];
    end

end

% Returns a list of empty points sorted by distance from the current point
function distanceAndPoints = closestEmptyPoints(currPoint, grid)
    emptyList = getAllEmptyCells(grid);
    distance = [];

    for index = 1:length(emptyList)
        emptyPoint = emptyList(index, :);
        distance = [distance; getChebyshevDistance(currPoint(1), currPoint(2), emptyPoint(1), emptyPoint(2))];
    end

    distanceAndPoints = [distance emptyList];
    distanceAndPoints = sortrows(distanceAndPoints);
end

% Returns the Chebyshev distance between two points
% This is the minimum number of moves a King needs to make to reach the destination
function dist = getChebyshevDistance(x1, y1, x2, y2)
    dist = max([abs(x2 - x1) abs(y2 - y1)]);
end

function validPoint = getClosestNewValidPoint(currAgentVal, currAgentLoc, currGrid, threshold)
    found = false;
    sortedDistList = closestEmptyPoints([currAgentLoc(1), currAgentLoc(2)], currGrid);

    % Loop through the distance list to find a valid point
    for index = 1:length(sortedDistList)

        % Get the X and Y values of the current empty location
        currEmptyLoc = sortedDistList(index, 2:3);

        % Check if the current empty location is valid
        if isValid(currAgentVal, currEmptyLoc, currGrid, threshold)
            % Found a valid point
            found = true;
            validPoint = currEmptyLoc;
            break
        end

    end

    if found == false
        % Unable to find a new valid point
        validPoint = currAgentLoc;
    end

end

% Check if a given cells neighbors are similar to a given value
function validity = isValid(val, loc, currGrid, threshold)

    % If the value is 0, it is always valid
    if val == 0
        validity = true;
        return
    end

    sameNeighbor = 0;
    validity = false;
    neighbors = getNeighborLocations(loc, currGrid);

    for indexNumber = 1:length(neighbors)
        currNeighborLoc = neighbors(indexNumber, :);

        if val == currGrid(currNeighborLoc(1), currNeighborLoc(2))
            sameNeighbor = sameNeighbor + 1;
        end

    end

    if sameNeighbor >= threshold
        validity = true;
    end

end

% Swaps two points (P1 and P2) in the grid and returns the new grid
function newGrid = swapPoints(P1, P2, currGrid)
    % Save a copy of point 2
    temp = currGrid(P2(1), P2(2));

    % Overwrite point 2 with point 1
    currGrid(P2(1), P2(2)) = currGrid(P1(1), P1(2));

    % Overwrite point 1 with the saved copy of point 2
    currGrid(P1(1), P1(2)) = temp;
    newGrid = currGrid;
end
