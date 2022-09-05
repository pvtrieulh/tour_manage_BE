from rest_framework import generics


class FilterBusiness(generics.ListAPIView):
    def get_queryset(self):
        business_id = self.request.business_id
        queryset = super(FilterBusiness, self).get_queryset()
        return queryset.filter(business_id=business_id)