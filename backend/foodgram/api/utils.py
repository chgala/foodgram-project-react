from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def download_shopping_list(request):
    recipe_list = request.user.current_user.all()
    buy_list = {}
    for list in recipe_list:
        ingredients = list.recipe.ingredients_in.all()
        for ingredient in ingredients:
            name = ingredient.ingredient.name
            amount = ingredient.amount
            measurement_unit = ingredient.ingredient.measurement_unit
            if name in buy_list.keys():
                buy_list[name]['amount'] += amount
            else:
                buy_list[name] = {}
                buy_list[name]['amount'] = amount
                buy_list[name]['measurement_unit'] = measurement_unit
    wishlist = ''
    for ingredient in buy_list:
        wishlist += f'{ingredient}'
        wishlist += f' ({buy_list[ingredient]["measurement_unit"]})   -   '
        wishlist += f'{buy_list[ingredient]["amount"]}'
        wishlist += ' \n'
    wishlist += ' \n'
    wishlist += ' \n'
    wishlist += 'Yours, Foodgram'
    response = HttpResponse(wishlist, 'Content-Type: application/pdf')
    response['Content-Disposition'] = 'attachment; filename="wishlist"'
    return response
