function [] = schelling()
clc;
clear;
close all;

threshold = 3; % update as necessary

% Initialize grid
grid = initGrid();

% Save and display First Grid
figure
displayGrid(grid, 'Initial Frame')
saveas(gcf, 'initialFrame.png')

mainModel(grid, threshold);

end

function grid = initGrid()
    % we want, X(1) and O(-1) to take 20% each of the grid
    % and blank space(0) remaining 60%
    % reducing these numbers we can say that out of 5 entries we want
    % three empty space(0), one X(1) and one O(-1)
    ratio = [0 0 0 -1 1]; % Proportion of the grid divided as per members
    temp = repmat(ratio, 1, 500); % randomly repeat this for 500 times
    temp = temp(randperm(numel(temp))); % Jumble up those entries
    grid = reshape(temp,[50,50]);
end

function [] = displayGrid(currGrid, titleString)
    imagesc(currGrid)
    cmap = flag(3);
    colormap(cmap);
    hold on
    entry = line(ones(3),ones(3));
    set(entry, {'color'}, mat2cell(cmap,ones(1,3),3));
    legend('X','empty','O')
    title(titleString)
    xlabel('Y')
    ylabel('X')
    hold off
end


function [] = mainModel(grid, threshold)
    gridSatisfactionFlag = false;
    imgSaveItr = 1;
%     while (gridSatisfactionFlag == false)
    while (imgSaveItr < 20)
        grid = mainShifting(grid, threshold);
        h=figure
        displayGrid(grid, sprintf('Frame%d',imgSaveItr))
        saveas(h,sprintf('Frame%d.png',imgSaveItr));
        imgSaveItr = imgSaveItr + 1;
    end
end

function grid = mainShifting(grid, threshold)
    unHappyLocations  = getAllUnhappy(grid, threshold);
    for sadMember = 1:length(unHappyLocations)       
        emptyPlaces = getAllEmptyPlaces(grid);
        currSadAgentLoc = unHappyLocations(sadMember,:);
        currSadAgentVal = grid(currSadAgentLoc(1), currSadAgentLoc(2));
        distAndPoints = closestEmptyPoints([currSadAgentLoc(1), currSadAgentLoc(2)], emptyPlaces);
        closestValidPoint = getNewValidPoint(currSadAgentVal, currSadAgentLoc, ??? , ??? , ??? );
        closestValidPoint = getNewValidPoint(???????);
        grid = swapPoints(???? , ??? , ??? );
    end
end




function unHappy = getAllUnhappy(currGrid, threshold)
    unHappy = [];
    S = size(currGrid);
    for x = 1:S(1)
        for y = 1:S(2)
            sameNeighbor = 0;
            currentMember = currGrid(x,y);
            if currentMember == 0
                continue
            else
                neighborIndices = getNeighborIndices(S, [x y]);
                for indexNumber = 1:length(neighborIndices)
                    currNeighbor = neighborIndices(indexNumber, :);
                    if currentMember == currGrid(currNeighbor(1),currNeighbor(2))
                        sameNeighbor = sameNeighbor + 1;
                    end
                end
                if sameNeighbor < threshold
                    unHappy = [unHappy; x, y];
                end
            end
        end
    end
end

function emptyCells = getAllEmptyPlaces(currGrid)
    emptyCells = [];
    S = size(currGrid);
    for x = 1:S(1)
        for y = 1:S(2)
            currentMember = currGrid(x,y);
            if currentMember == 0
                emptyCells = [emptyCells; x, y];
            end
        end
    end
end

function neighborIndices = getNeighborIndices(gridSize, own)
    neighborIndices = [];
    S = gridSize;
    x = own(1);
    y = own(2);
    if x < S(1)
        neighborIndices = [neighborIndices; x+1, y];
        if y>1
            neighborIndices = [neighborIndices; x+1, y-1];
        end
        if y<S(2)
            neighborIndices = [neighborIndices; x+1, y+1];
        end
    end

    if y < S(2)
        neighborIndices = [neighborIndices; x, y+1];
    end

    if x > 1
        neighborIndices = [neighborIndices; x-1, y];
        if y>1
            neighborIndices = [neighborIndices; x-1, y-1];
        end
        if y<S(2)
            neighborIndices = [neighborIndices; x-1, y+1];
        end
    end

    if y > 1 && y < S(2)
        neighborIndices = [neighborIndices; x, y-1];
    end

end

function distanceAndPoints = closestEmptyPoints(currPoint, emptyList)
    distance = [];
    for index = 1: length(emptyList)
        emptyPoint = emptyList(index,:);
        distance = [distance; get8Distance(currPoint(1), currPoint(2), emptyPoint(1), emptyPoint(2))];
    end
    distanceAndPoints = [distance emptyList];
    distanceAndPoints = sortrows(distanceAndPoints);
end

function dist = get8Distance(x1, y1, x2, y2)
    dist = max([abs(x2-x1) abs(y2-y1)]);
end

function validPoint = getNewValidPoint(currAgentVal, currAgentLoc, distList, currGrid, threshold)
    validFlag = false;
    for index = 1:length(distList)
        currEmptyLoc = distList(index,2:3);
        validFlag = checkValidity(currAgentVal, currEmptyLoc, currGrid, threshold);
        if validFlag == true
            validPoint = currEmptyLoc;
            break
        end
    end
    if validFlag == false
        validPoint = currAgentLoc;
    end
end

function validity = checkValidity(val, loc, currGrid, threshold)
    S = size(currGrid);
    sameNeighbor = 0;
    validity = false;
    neighbors = getNeighborIndices(S, loc);
    for indexNumber = 1:length(neighbors)
        currNeighborLoc = neighbors(indexNumber, :);
        if val == currGrid(currNeighborLoc(1),currNeighborLoc(2))
            sameNeighbor = sameNeighbor + 1;
        end
    end
    if sameNeighbor >= threshold
        validity = true;
    end
end

function newGrid = swapPoints(P1, P2, currGrid)
    temp = currGrid(P2(1), P2(2));
    currGrid(P2(1), P2(2)) = currGrid(P1(1), P1(2));
    currGrid(P1(1), P1(2)) = temp;
    newGrid = currGrid;
end