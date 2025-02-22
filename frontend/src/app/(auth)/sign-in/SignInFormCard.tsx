import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import SocialAuthentication from "@/features/auth/SocialAuthentication";

const SignInFormCard = () => {
    return (
        <Card>
            <CardHeader>
                <CardTitle>Welcom Back!</CardTitle>
                <CardDescription>
                    Glad to have you back. PLease log in to continue.
                </CardDescription>
            </CardHeader>
            <CardContent>{/* Sign In Form */}</CardContent>
            <CardFooter>
                <SocialAuthentication />
            </CardFooter>
        </Card>
    );
};

export default SignInFormCard;
