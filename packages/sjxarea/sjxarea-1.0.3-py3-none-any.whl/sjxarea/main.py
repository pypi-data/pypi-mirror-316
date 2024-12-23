import sjxarea
a,b,c=int(input().split())
def area(a,b,c):

   s=(a+b+c)/2
   area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
   return area
if __name__ == '__main__':
    area(a,b,c)
