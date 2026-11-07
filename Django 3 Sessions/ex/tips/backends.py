from django.contrib.auth.backends import ModelBackend


class ReputationBackend(ModelBackend):
    """Keep admin grants and add privileges earned from current votes."""

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        permissions = self.get_user_permissions(user_obj) | self.get_group_permissions(user_obj)
        reputation = user_obj.reputation
        if reputation >= 15:
            permissions.add("tips.downvote_tip")
        if reputation >= 30:
            permissions.add("tips.delete_tip")
        return permissions
