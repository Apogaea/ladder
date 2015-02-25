class WithMatchMixin(object):
    def get_context_data(self, **kwargs):
        context = super(WithMatchMixin, self).get_context_data(**kwargs)
        context['pending_match'] = self.object.get_pending_match()
        context['accepted_match'] = self.object.get_accepted_match()
        return context
