def selection_sort(items):
    n = len(items)
    
    for i in range(n):
        min_index = i
        
        for j in range(i + 1, n):
            if items[j] < items[min_index]:
                min_index = j
                
        if min_index != i:
            items[i], items[min_index] = items[min_index], items[i]
            
    return items