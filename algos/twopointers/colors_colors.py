def sort_colors(colors):
    
    # Replace this placeholder return statement with your code
    
    sin = 0
    
    des = len(colors)-1
    
    curr = 0
    
    while sin <= des: 
        
        if colors[curr] == 0:
            colors[curr], colors[sin] =  colors[sin] , colors[curr]
            sin = sin + 1
            curr = curr + 1
            
        elif  colors[curr] == 2:
            colors[curr], colors[des] = colors[des], colors[curr]
            des = des - 1
        
        else: 
            curr = curr + 1
            
        
        
        

        
        
 

    return colors