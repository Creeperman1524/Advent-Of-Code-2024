def solve(input):
    parseRules = True
    rules = []
    pages = []

    # Parses the rules and pages
    for i in range(len(input)):
        line = input[i]

        # Divider
        if len(line) == 0:
            parseRules = False
            continue

        if parseRules:
            rules.append(line.split("|"))
        else:
            pages.append(line.split(","))

    total = 0

    for update in pages:
        # update = current edition we are looking at

        valid = True
        # Tries all the rules for this edition
        for rule in rules:

            # Checks if the rule is valid for this update
            if rule[0] in update and rule[1] in update:
                if update.index(rule[0]) > update.index(rule[1]):
                    valid = False

        if valid:
            # Adds the middle value
            total += int(update[len(update) // 2])

    return total
